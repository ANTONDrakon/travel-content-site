"""
PhotoManifestWriter — persists photo-to-hotel mapping as JSON.

Each manifest entry is self-contained with full provenance.
"""

import json
from pathlib import Path
from typing import List

from photo_pipeline.interfaces import PhotoManifestWriter


class PhotoManifestWriter(PhotoManifestWriter):

    def write(self, entries: List[dict], path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def read(self, path: Path) -> List[dict]:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return []

    @staticmethod
    def build_entry(
        hotel_name: str,
        slug: str,
        city_slug: str,
        country_slug: str,
        provider: str,
        provider_hotel_id: str,
        image_url: str,
        local_path: str,
        alt_text: str,
        caption: str,
        attribution: str,
        source_page_url: str,
        verification_score: float,
        verified: bool,
        width: int = 800,
        height: int = 500,
    ) -> dict:
        return {
            "hotel_name": hotel_name,
            "slug": slug,
            "city_slug": city_slug,
            "country_slug": country_slug,
            "provider": provider,
            "provider_hotel_id": provider_hotel_id,
            "image_url": image_url,
            "local_path": local_path,
            "src": local_path,
            "alt": alt_text,
            "caption": caption,
            "attribution": attribution,
            "source_page_url": source_page_url,
            "verification_score": verification_score,
            "verified": verified,
            "width": width,
            "height": height,
        }
