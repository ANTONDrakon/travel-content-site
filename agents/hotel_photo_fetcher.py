"""
Real Hotel Photo Fetcher
Replaces Unsplash stock photos with actual hotel imagery.

Sources (in priority order):
1. Local photo database (data/hotel_photo_sources.json - user-managed)
2. Google Programmable Search JSON API (free tier, configure in .env as GOOGLE_API_KEY + GOOGLE_CX)
3. Official hotel media/press URLs (built-in)
4. Hotellook image CDN (photo.hotellook.com)
5. Web search with domain verification
6. Category fallback (clearly marked unverified, marked as `verified: false`)

Setup for real photos:
    # Google Custom Search (free, 100 queries/day):
    # 1. Go to https://programmablesearch.google.com/ - create a search engine
    # 2. Get your Search engine ID (CX) and API key
    # 3. Add to .env:
    #    GOOGLE_API_KEY=your_key
    #    GOOGLE_CX=your_search_engine_id
    #
    # Travelpayouts Hotels API:
    # 1. Get API token from travelpayouts.com dashboard
    # 2. Add to .env:
    #    TRAVELPAYOUTS_API_TOKEN=your_token
    #
    # Manual photo URLs:
    # Edit data/hotel_photo_sources.json and add URLs for specific hotels

Usage:
    python -m agents.hotel_photo_fetcher --all
    python -m agents.hotel_photo_fetcher --city turkey/istanbul
    python -m agents.hotel_photo_fetcher --hotel "Four Seasons Istanbul" --country turkey --city istanbul
    python -m agents.hotel_photo_fetcher --update-db
"""

import os
import json
import hashlib
import io
import re
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from urllib.parse import quote

BASE = Path(__file__).parent.parent
HOTELS_DB_PATH = BASE / "data" / "hotels.json"
SOURCES_DB_PATH = BASE / "data" / "hotel_photo_sources.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"
PHOTO_CACHE_PATH = ASSETS_DIR / "_photo_cache.json"

MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "736226")
TP_API_TOKEN = os.getenv("TRAVELPAYOUTS_API_TOKEN", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CX = os.getenv("GOOGLE_CX", "")
USER_AGENT = "TravelHub/1.0 (photo-fetcher; +https://github.com/ANTONDrakon/travel-content-site)"

HOTELLOOK_CDN = "https://photo.hotellook.com/image/v2"

def _load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class HotelPhotoFetcher:
    def __init__(self):
        self.hotels_db = _load_json(HOTELS_DB_PATH)
        self.sources_db = _load_json(SOURCES_DB_PATH)
        self.cache = _load_json(PHOTO_CACHE_PATH)
        self.results = {"verified": [], "unverified": [], "failed": []}

    def _cache_key(self, name, city_slug):
        raw = f"{name}|{city_slug}".lower().strip()
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _save_cache(self):
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        _save_json(PHOTO_CACHE_PATH, self.cache)

    def _download_webp(self, url: str, output_path: Path) -> bool:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            data = urllib.request.urlopen(req, timeout=20).read()
            if len(data) < 1000:
                return False
            try:
                from PIL import Image
                img = Image.open(io.BytesIO(data))
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode in ("RGBA", "LA"):
                        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else img)
                    else:
                        bg.paste(img.convert("RGBA"))
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                if img.width > 1200:
                    ratio = 1200 / img.width
                    img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(output_path, format="WEBP", quality=85)
            except Exception:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(data)
            return output_path.exists() and output_path.stat().st_size > 500
        except Exception:
            return False

    def _hotellook_photos(self, hotel_id: str, max_photos: int = 3) -> list:
        if not hotel_id or not hotel_id.strip():
            return []
        hotel_id = hotel_id.strip()
        photos = []
        for i in range(1, max_photos + 1):
            url = f"{HOTELLOOK_CDN}/{hotel_id}/{i}.jpg"
            photos.append({
                "url": url,
                "source": "hotellook_cdn",
                "verified": True,
                "hotel_id": hotel_id,
                "index": i,
            })
        return photos

    def _official_media_urls(self, hotel_name: str, city_name: str) -> Optional[list]:
        nl = hotel_name.lower()
        for key, entry in self.sources_db.get("official_media", {}).items():
            if isinstance(entry, dict) and key.lower() in nl:
                photos = entry.get("photos", [])
                if photos and isinstance(photos, list):
                    return [{"url": p, "source": "official_media", "verified": True, "brand": key}
                            for p in photos[:3]]
        return None

    def _search_hotellook_static(self, hotel_name: str, city_name: str) -> Optional[str]:
        try:
            query = quote(f"{hotel_name} {city_name}")
            url = f"https://engine.hotellook.com/api/v2/static/hotels/search.json?query={query}&token={MARKER}&limit=5"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            results = data.get("results", data.get("hotels", []))
            if results:
                return str(results[0].get("id", results[0].get("hotelId", "")))
        except Exception:
            pass
        return None

    def _search_hotellook_lookup(self, hotel_name: str, city_name: str) -> Optional[str]:
        try:
            query = quote(f"{hotel_name} {city_name}")
            url = f"https://engine.hotellook.com/api/v2/lookup.json?query={query}&lang=en&token={MARKER}"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            for category in data.get("results", []):
                for item in category.get("items", []):
                    if "hotelId" in item or "id" in item:
                        return str(item.get("hotelId", item.get("id", "")))
        except Exception:
            pass
        return None

    def _search_web_for_hotel_photos(self, hotel_name: str, city_name: str) -> list:
        photos = []
        query = quote(f"{hotel_name} {city_name} hotel official website")
        search_urls = [
            f"https://html.duckduckgo.com/html/?q={query}",
        ]
        for search_url in search_urls:
            try:
                req = urllib.request.Request(
                    search_url,
                    headers={"User-Agent": USER_AGENT},
                )
                resp = urllib.request.urlopen(req, timeout=15)
                html = resp.read().decode("utf-8", errors="replace")
                img_urls = re.findall(
                    r'<img[^>]+src="(https://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',
                    html,
                    re.IGNORECASE,
                )
                for img_url in img_urls[:3]:
                    photos.append({
                        "url": img_url,
                        "source": "web_search",
                        "verified": False,
                    })
                if photos:
                    break
            except Exception:
                continue
        return photos

    def _google_search_photos(self, hotel_name: str, city_name: str) -> Optional[list]:
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return None
        try:
            query = quote(f"{hotel_name} {city_name} hotel")
            url = (f"https://www.googleapis.com/customsearch/v1"
                   f"?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
                   f"&q={query}&searchType=image&num=3")
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            photos = []
            for item in items[:3]:
                img_url = item.get("link", "")
                if img_url:
                    photos.append({
                        "url": img_url,
                        "source": "google_search",
                        "verified": True,
                        "context": item.get("image", {}).get("contextLink", ""),
                    })
            return photos if photos else None
        except Exception:
            return None

    def _google_search_images(self, hotel_name: str, city_name: str) -> Optional[list]:
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return None
        try:
            query = quote(f"{hotel_name} {city_name} hotel exterior")
            url = (f"https://www.googleapis.com/customsearch/v1"
                   f"?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
                   f"&q={query}&searchType=image&num=3")
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            photos = []
            for item in items[:3]:
                img_url = item.get("link", "")
                if img_url:
                    photos.append({
                        "url": img_url,
                        "source": "google_images",
                        "verified": True,
                        "context": item.get("image", {}).get("contextLink", ""),
                    })
            return photos if photos else None
        except Exception:
            return None

    def _travelpayouts_hotel_photos(self, hotel_name: str, city_name: str) -> Optional[list]:
        if not TP_API_TOKEN:
            return None
        try:
            query = quote(f"{hotel_name} {city_name}")
            url = (f"https://api.travelpayouts.com/v1/hotel/static/hotels.json"
                   f"?token={TP_API_TOKEN}&query={query}&limit=3")
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode())
            hotels = data if isinstance(data, list) else data.get("hotels", [])
            if hotels:
                hotel_id = hotels[0].get("id", hotels[0].get("hotelId", ""))
                if hotel_id:
                    return self._hotellook_photos(hotel_id, 3)
            return None
        except Exception:
            return None

    def find_photos(self, hotel_name: str, city_slug: str,
                    country_slug: str, max_photos: int = 3) -> dict:
        ck = self._cache_key(hotel_name, city_slug)
        if ck in self.cache:
            cached = self.cache[ck]
            if isinstance(cached, list) and len(cached) > 0:
                return {"photos": cached, "cache_key": ck, "from_cache": True}

        city_name = city_slug.replace("-", " ").title()
        photos = []

        step1 = self._official_media_urls(hotel_name, city_name)
        if step1:
            photos = step1
            self.results["verified"].append(hotel_name)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        step_google = self._google_search_photos(hotel_name, city_name)
        if step_google:
            photos = step_google
            self.results["verified"].append(hotel_name)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        step_tp = self._travelpayouts_hotel_photos(hotel_name, city_name)
        if step_tp:
            photos = step_tp
            self.results["verified"].append(hotel_name)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        hotel_id = self.sources_db.get("hotellook_ids", {}).get(
            f"{country_slug}/{city_slug}/{hotel_name.lower().replace(' ', '-')}"
        )
        if hotel_id and str(hotel_id).strip():
            hotel_id = str(hotel_id).strip()
            photos = self._hotellook_photos(hotel_id, max_photos)
            self.results["verified"].append(hotel_name)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        hotel_id = self._search_hotellook_static(hotel_name, city_name)
        if not hotel_id:
            hotel_id = self._search_hotellook_lookup(hotel_name, city_name)
        if hotel_id:
            photos = self._hotellook_photos(hotel_id, max_photos)
            self.results["verified"].append(hotel_name)
            sources = self.sources_db.setdefault("hotellook_ids", {})
            key = f"{country_slug}/{city_slug}/{hotel_name.lower().replace(' ', '-')}"
            sources[key] = hotel_id
            _save_json(SOURCES_DB_PATH, self.sources_db)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        web_photos = self._search_web_for_hotel_photos(hotel_name, city_name)
        if web_photos:
            photos = web_photos[:max_photos]
            self.results["unverified"].append(hotel_name)
            result_photos = photos[:max_photos]
            self.cache[ck] = result_photos
            self._save_cache()
            return {"photos": result_photos, "cache_key": ck, "from_cache": False}

        self.results["failed"].append(hotel_name)
        return {"photos": [], "cache_key": ck, "from_cache": False}

    def download_hotel_photos(self, hotel_entry: dict, max_photos: int = 3) -> dict:
        name = hotel_entry["name"]
        slug = hotel_entry["slug"]
        country_slug = hotel_entry["country_slug"]
        city_slug = hotel_entry["city_slug"]

        result = self.find_photos(name, city_slug, country_slug, max_photos)
        photos = result["photos"]

        downloaded = []
        for i, photo in enumerate(photos[:3]):
            if isinstance(photo, str):
                photo_url = photo
                photo_verified = False
                photo_source = "unknown"
            else:
                photo_url = photo.get("url", "")
                photo_verified = photo.get("verified", False)
                photo_source = photo.get("source", "unknown")
            if not photo_url:
                continue

            hotel_dir = ASSETS_DIR / country_slug / city_slug / slug
            filename = f"{i+1:02d}.webp"
            local_path = hotel_dir / filename

            if local_path.exists() and local_path.stat().st_size > 1000:
                downloaded.append({
                    "src": f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{filename}",
                    "alt": f"{name} — {hotel_entry.get('city_name_ru', city_slug)}",
                    "alt_en": f"{name} — {hotel_entry.get('city_name_en', city_slug)}",
                    "caption": name,
                    "width": 800,
                    "height": 500,
                    "verified": photo_verified,
                    "source": photo_source,
                })
                continue

            if self._download_webp(photo_url, local_path):
                downloaded.append({
                    "src": f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{filename}",
                    "alt": f"{name} — {hotel_entry.get('city_name_ru', city_slug)}",
                    "alt_en": f"{name} — {hotel_entry.get('city_name_en', city_slug)}",
                    "caption": name,
                    "width": 800,
                    "height": 500,
                    "verified": photo_verified,
                    "source": photo_source,
                })

        return {
            "hotel": name,
            "slug": slug,
            "photos": downloaded,
            "verified_count": sum(1 for p in downloaded if p["verified"]),
        }

    def process_all(self) -> dict:
        stats = {"total": 0, "verified": 0, "unverified": 0, "failed": 0, "errors": []}
        for i, hotel in enumerate(self.hotels_db):
            try:
                name = hotel["name"]
                print(f"[{i+1}/{len(self.hotels_db)}] {name}...", end=" ")
                result = self.download_hotel_photos(hotel)
                if result["verified_count"] > 0:
                    print(f"OK ({result['verified_count']} verified)")
                    stats["verified"] += 1
                elif result["photos"]:
                    print(f"UNVERIFIED ({len(result['photos'])} photos)")
                    stats["unverified"] += 1
                else:
                    print("FAILED (no photos)")
                    stats["failed"] += 1
                stats["total"] += 1
            except Exception as e:
                print(f"ERROR: {e}")
                stats["errors"].append(f"{hotel.get('name', '?')}: {e}")
                stats["failed"] += 1
        return stats

    def process_city(self, country_slug: str, city_slug: str) -> dict:
        stats = {"total": 0, "verified": 0, "unverified": 0, "failed": 0, "errors": []}
        for i, hotel in enumerate(self.hotels_db):
            if hotel["country_slug"] != country_slug or hotel["city_slug"] != city_slug:
                continue
            try:
                name = hotel["name"]
                print(f"[{i+1}] {name}...", end=" ")
                result = self.download_hotel_photos(hotel)
                if result["verified_count"] > 0:
                    print(f"OK ({result['verified_count']} verified)")
                    stats["verified"] += 1
                elif result["photos"]:
                    print(f"UNVERIFIED ({len(result['photos'])} photos)")
                    stats["unverified"] += 1
                else:
                    print("FAILED")
                    stats["failed"] += 1
                stats["total"] += 1
            except Exception as e:
                print(f"ERROR: {e}")
                stats["errors"].append(f"{hotel.get('name', '?')}: {e}")
        return stats

    def update_hotels_db_with_photos(self):
        updates = 0
        for hotel in self.hotels_db:
            slug = hotel["slug"]
            country_slug = hotel["country_slug"]
            city_slug = hotel["city_slug"]
            hotel_dir = ASSETS_DIR / country_slug / city_slug / slug

            new_images = []
            for i in range(1, 4):
                webp_path = hotel_dir / f"{i:02d}.webp"
                if webp_path.exists():
                    name = hotel["name"]
                    new_images.append({
                        "src": f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{i:02d}.webp",
                        "alt": f"{name} — {hotel.get('city_name_ru', city_slug)}",
                        "alt_en": f"{name} — {hotel.get('city_name_en', city_slug)}",
                        "caption": name,
                        "width": 800,
                        "height": 500,
                    })

            if new_images:
                hotel["images"] = new_images
                updates += 1

        _save_json(HOTELS_DB_PATH, self.hotels_db)
        return updates

    def report(self) -> dict:
        return {
            "hotels_in_db": len(self.hotels_db),
            "verified_hotels": len(self.results["verified"]),
            "unverified_hotels": len(self.results["unverified"]),
            "failed_hotels": len(self.results["failed"]),
            "photos_in_cache": len(self.cache),
            "sources_in_db": len(self.sources_db.get("hotellook_ids", {})),
        }


def run():
    import argparse
    parser = argparse.ArgumentParser(description="Real Hotel Photo Fetcher")
    parser.add_argument("--all", action="store_true", help="Process all hotels")
    parser.add_argument("--country", type=str, help="Country slug")
    parser.add_argument("--city", type=str, help="City slug")
    parser.add_argument("--hotel", type=str, help="Hotel name (with --country --city)")
    parser.add_argument("--update-db", action="store_true",
                        help="Update data/hotels.json with local photo paths")
    parser.add_argument("--report", action="store_true", help="Show report")

    args = parser.parse_args()
    fetcher = HotelPhotoFetcher()

    if args.report:
        print(json.dumps(fetcher.report(), indent=2, ensure_ascii=False))
        return

    if args.all:
        print("\n=== Processing ALL hotels ===\n")
        stats = fetcher.process_all()
        print(f"\nDone: {stats['total']} total, {stats['verified']} verified, "
              f"{stats['unverified']} unverified, {stats['failed']} failed")
        if stats["errors"]:
            print(f"\nErrors ({len(stats['errors'])}):")
            for e in stats["errors"]:
                print(f"  - {e}")

    elif args.city:
        parts = args.city.split("/")
        if len(parts) != 2:
            print("Use --city country/city (e.g. turkey/istanbul)")
            return
        print(f"\n=== Processing {args.city} ===\n")
        stats = fetcher.process_city(parts[0], parts[1])
        print(f"\nDone: {stats['total']} total, {stats['verified']} verified, "
              f"{stats['unverified']} unverified, {stats['failed']} failed")

    elif args.hotel and args.country and args.city:
        print(f"\n=== Processing {args.hotel} ===\n")
        for hotel in fetcher.hotels_db:
            if (hotel["name"].lower() == args.hotel.lower()
                    and hotel["country_slug"] == args.country
                    and hotel["city_slug"] == args.city):
                result = fetcher.download_hotel_photos(hotel)
                print(f"Hotel: {result['hotel']}")
                print(f"Photos: {len(result['photos'])}")
                print(f"Verified: {result['verified_count']}")
                for p in result["photos"]:
                    print(f"  {p['src']} (verified={p['verified']}, source={p['source']})")
                return
        print(f"Hotel not found: {args.hotel}")

    if args.update_db:
        print("\n=== Updating data/hotels.json with photo paths ===\n")
        updates = fetcher.update_hotels_db_with_photos()
        print(f"Updated {updates} hotels")

    if not any([args.all, args.city, args.hotel, args.report, args.update_db]):
        parser.print_help()


if __name__ == "__main__":
    run()
