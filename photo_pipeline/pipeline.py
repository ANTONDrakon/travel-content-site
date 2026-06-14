"""
PhotoPipeline — orchestrator that connects providers → verifier → downloader → uploader → manifest.

Usage:
    from photo_pipeline import PhotoPipeline
    pipeline = PhotoPipeline()
    results = pipeline.process_hotel(hotel_info)
    pipeline.process_all_hotels()
"""

import json
import time
from pathlib import Path
from typing import List, Optional, Dict

from photo_pipeline.models import HotelInfo, PhotoMetadata
from photo_pipeline.interfaces import PhotoProvider, PhotoVerifier, PhotoDownloader, PhotoUploader
from photo_pipeline.verifier import DefaultPhotoVerifier
from photo_pipeline.downloader import DefaultPhotoDownloader
from photo_pipeline.uploader import LocalPhotoUploader
from photo_pipeline.manifest import PhotoManifestWriter
from photo_pipeline.providers import TravelpayoutsProvider, GooglePlacesProvider, ManualProvider

BASE_DIR = Path(__file__).parent.parent


class PhotoPipeline:
    """Orchestrates the full photo ingestion pipeline."""

    def __init__(
        self,
        providers: Optional[List[PhotoProvider]] = None,
        verifier: Optional[PhotoVerifier] = None,
        downloader: Optional[PhotoDownloader] = None,
        uploader: Optional[PhotoUploader] = None,
        manifest_writer: Optional[PhotoManifestWriter] = None,
        staging_dir: str = "data/photo_staging",
        manifest_path: str = "data/photo_manifest.json",
        hotels_db_path: str = "data/hotels.json",
    ):
        self.providers = providers or [
            ManualProvider(),
            TravelpayoutsProvider(),
            GooglePlacesProvider(),
        ]
        self.verifier = verifier or DefaultPhotoVerifier()
        self.downloader = downloader or DefaultPhotoDownloader()
        self.uploader = uploader or LocalPhotoUploader()
        self.manifest_writer = manifest_writer or PhotoManifestWriter()
        self.staging_dir = Path(staging_dir)
        self.manifest_path = Path(manifest_path)
        self.hotels_db_path = Path(hotels_db_path)
        self.stats = {"processed": 0, "verified": 0, "rejected": 0, "errors": 0}

    def process_hotel(self, hotel: HotelInfo) -> dict:
        """Process a single hotel through the full pipeline."""
        self.stats["processed"] += 1
        result = {
            "hotel": hotel.name,
            "city": hotel.city,
            "country": hotel.country,
            "status": "NEEDS_REVIEW",
            "photos": [],
            "errors": [],
        }

        # Step 1: Collect candidates from all providers
        candidates: List[PhotoMetadata] = []
        for provider in self.providers:
            try:
                photos = provider.search(hotel)
                candidates.extend(photos)
            except Exception as e:
                result["errors"].append(f"{provider.provider_name}: {e}")

        if not candidates:
            result["status"] = "NO_CANDIDATES"
            return result

        # Step 2: Verify each candidate
        verified_photos: List[PhotoMetadata] = []
        for candidate in candidates:
            try:
                vr = self.verifier.verify(candidate, hotel)
                if vr.passed:
                    verified_photos.append(vr.photo)
                else:
                    result["errors"].append(
                        f"rejected: {vr.reason} (score={vr.score})"
                    )
            except Exception as e:
                result["errors"].append(f"verify error: {e}")

        if not verified_photos:
            result["status"] = "REJECTED"
            self.stats["rejected"] += 1
            return result

        # Step 3: Sort by score, pick primary + gallery
        verified_photos.sort(key=lambda p: p.verification_score, reverse=True)
        primary = verified_photos[0]
        gallery = verified_photos[1:]

        # Step 4: Download primary + gallery
        staging = self.staging_dir / hotel.country / hotel.slug
        staging.mkdir(parents=True, exist_ok=True)

        downloaded = []
        for idx, photo in enumerate([primary] + gallery[:4]):
            local = self.downloader.download(photo, staging)
            if not local:
                result["errors"].append(f"download failed for {photo.image_url[:60]}")
                continue
            # Step 5: Upload to site assets
            remote_key = f"{hotel.country}/{hotel.slug}/{photo.provider}_{idx + 1:02d}.webp"
            public_url = self.uploader.upload(local, remote_key)
            alt_text = LocalPhotoUploader.generate_alt_text(photo)
            caption = LocalPhotoUploader.generate_caption(photo)
            downloaded.append({
                "src": public_url,
                "alt": alt_text,
                "alt_en": LocalPhotoUploader.generate_alt_text(photo, "en"),
                "caption": caption,
                "provider": photo.provider,
                "provider_hotel_id": photo.provider_hotel_id,
                "source_page_url": photo.source_page_url,
                "attribution": photo.attribution,
                "verification_score": photo.verification_score,
                "verified": photo.verified,
                "width": photo.width or 800,
                "height": photo.height or 500,
            })

        if not downloaded:
            result["status"] = "DOWNLOAD_FAILED"
            self.stats["errors"] += 1
            return result

        result["status"] = "VERIFIED"
        result["photos"] = downloaded
        self.stats["verified"] += 1
        return result

    def process_all_hotels(self) -> List[dict]:
        """Process all hotels from data/hotels.json."""
        if not self.hotels_db_path.exists():
            print(f"Hotels DB not found: {self.hotels_db_path}")
            return []

        hotels = json.loads(self.hotels_db_path.read_text(encoding="utf-8"))
        results = []
        manifest_entries = []

        for i, h in enumerate(hotels):
            if not isinstance(h, dict) or "name" not in h:
                continue
            name = h.get("name", "")
            print(f"[{i + 1}/{len(hotels)}] {name}...", end=" ", flush=True)

            hotel_info = HotelInfo(
                name=name,
                city=h.get("city_name_en", h.get("city_slug", "")),
                country=h.get("country_slug", ""),
                slug=h.get("slug", ""),
                address=h.get("address", h.get("description", "")),
            )
            try:
                result = self.process_hotel(hotel_info)
                results.append(result)
                if result["status"] == "VERIFIED":
                    print(f"VERIFIED ({len(result['photos'])} photos)")
                    for p in result["photos"]:
                        manifest_entries.append(
                            PhotoManifestWriter.build_entry(
                                hotel_name=name,
                                slug=hotel_info.slug,
                                city_slug=h.get("city_slug", ""),
                                country_slug=hotel_info.country,
                                provider=p["provider"],
                                provider_hotel_id=p["provider_hotel_id"],
                                image_url=p.get("source_page_url", ""),
                                local_path=p["src"],
                                alt_text=p["alt"],
                                caption=p["caption"],
                                attribution=p["attribution"],
                                source_page_url=p["source_page_url"],
                                verification_score=p["verification_score"],
                                verified=p["verified"],
                                width=p["width"],
                                height=p["height"],
                            )
                        )
                elif result["status"] == "REJECTED":
                    print(f"REJECTED ({len(result.get('errors', []))} errors)")
                elif result["status"] == "NO_CANDIDATES":
                    print("NO CANDIDATES")
                else:
                    print(result["status"])
            except Exception as e:
                print(f"ERROR: {e}")
                results.append({
                    "hotel": name,
                    "status": "ERROR",
                    "errors": [str(e)],
                    "photos": [],
                })

            time.sleep(0.5)  # rate limiting

        # Write manifest
        self.manifest_writer.write(manifest_entries, self.manifest_path)
        print(f"\nManifest written: {self.manifest_path} ({len(manifest_entries)} photos)")

        # Update hotels.json with verified photos
        self._update_hotels_db(manifest_entries)

        print(f"\nStats: {self.stats['processed']} processed, "
              f"{self.stats['verified']} verified, "
              f"{self.stats['rejected']} rejected, "
              f"{self.stats['errors']} errors")
        return results

    def _update_hotels_db(self, manifest_entries: List[dict]):
        if not manifest_entries:
            return
        hotels = json.loads(self.hotels_db_path.read_text(encoding="utf-8"))
        by_key = {}
        for e in manifest_entries:
            key = (e["country_slug"], e["city_slug"], e["slug"])
            by_key.setdefault(key, []).append(e)

        updates = 0
        for h in hotels:
            if not isinstance(h, dict):
                continue
            key = (h.get("country_slug", ""), h.get("city_slug", ""), h.get("slug", ""))
            entries = by_key.get(key, [])
            if not entries:
                continue
            new_images = []
            for e in entries:
                new_images.append({
                    "src": e["src"],
                    "alt": e["alt"],
                    "alt_en": e.get("alt_en", e["alt"]),
                    "caption": e["caption"],
                    "width": e["width"],
                    "height": e["height"],
                    "verified": e["verified"],
                    "source": e["provider"],
                    "attribution": e["attribution"],
                    "provider_hotel_id": e["provider_hotel_id"],
                    "verification_score": e["verification_score"],
                })
            if new_images:
                h["images"] = new_images
                updates += 1

        self.hotels_db_path.write_text(
            json.dumps(hotels, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Updated {updates} hotels in {self.hotels_db_path}")

    def summary(self) -> dict:
        return dict(self.stats)
