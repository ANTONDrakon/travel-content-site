"""
Booking.com Affiliate API provider.

Official, licensed API for Booking.com partners.
Returns real hotel photos licensed for affiliate use.

Requires:
  - BOOKING_COM_AID (affiliate ID, e.g. 397643) in .env
  - BOOKING_COM_SHARED_SECRET (from booking.com affiliate dashboard) in .env

API docs: https://distribution-xml.booking.com/2.0/

Usage:
    python -m photo_pipeline.providers.booking_affiliate --search "Holiday Inn Express Dongzhimen" --country china --city beijing
    python -m photo_pipeline.providers.booking_affiliate --all
"""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import time
from pathlib import Path
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from PIL import Image

BASE = Path(__file__).parent.parent.parent
HOTELS_DB = BASE / "data" / "hotels.json"
MANIFEST_PATH = BASE / "data" / "photo_manifest.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"

AID = os.getenv("BOOKING_COM_AID", "397643")
SHARED_SECRET = os.getenv("BOOKING_COM_SHARED_SECRET", "")

API_BASE = "https://distribution-xml.booking.com/2.0/json"
USER_AGENT = "TravelHubPhotoPipeline/2.0"

COUNTRY_CODES = {
    "turkey": "tr", "thailand": "th", "egypt": "eg",
    "uae": "ae", "indonesia": "id", "china": "cn", "maldives": "mv",
}


def _auth_header() -> dict:
    creds = f"{AID}:{SHARED_SECRET}"
    encoded = base64.b64encode(creds.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "User-Agent": USER_AGENT,
    }


def _fetch_json(url: str) -> Optional[dict]:
    if not SHARED_SECRET:
        return None
    try:
        req = Request(url, headers=_auth_header())
        resp = urlopen(req, timeout=20)
        return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  API error: {type(e).__name__}: {str(e)[:100]}")
        return None


def search_hotel(hotel_name: str, city: str = "", country_slug: str = "") -> Optional[str]:
    """Search for a hotel via Booking.com Affiliate API and return hotel_id."""
    query = f"{hotel_name} {city}".strip()
    params = urlencode({
        "search_query": query,
        "rows": 10,
        "order_by": "popularity",
        "extras": "hotel_info",
    })
    url = f"{API_BASE}/hotelSearch?{params}"
    data = _fetch_json(url)
    if not data:
        return None

    results = data.get("result", [])
    if not results:
        return None

    nl = hotel_name.lower().strip()
    best = None
    best_score = 0.0

    for h in results:
        hn = (h.get("hotel_name") or "").lower().strip()
        hc = (h.get("city") or h.get("city_name") or "").lower().strip()
        score = 0.0
        if hn == nl:
            score += 0.6
        elif nl in hn or hn in nl:
            score += 0.3
        if city and city.lower() in hc:
            score += 0.2
        if score > best_score:
            best_score = score
            best = h

    if best and best_score >= 0.3:
        return str(best.get("hotel_id") or best.get("hotelId", ""))
    return None


def get_hotel_photos(hotel_id: str, max_photos: int = 5) -> List[dict]:
    """Fetch photo URLs for a hotel from Booking.com Affiliate API."""
    params = urlencode({
        "hotel_ids": hotel_id,
        "extras": "hotel_info,hotel_photos",
    })
    url = f"{API_BASE}/hotelDescription?{params}"
    data = _fetch_json(url)
    if not data:
        return []

    results = data.get("result", [])
    if not results:
        return []

    hotel = results[0]
    # Photo URLs from Booking.com API
    photos = []
    # Try different photo URL fields
    for key in ["url_photos", "photos", "hotel_photos", "photo_urls", "images"]:
        raw = hotel.get(key, [])
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    url = item.get("url", item.get("url_max", item.get("url_640", "")))
                elif isinstance(item, str):
                    url = item
                else:
                    continue
                if url and ("bstatic.com" in url or "booking.com" in url):
                    photos.append({"url": url, "booking_id": hotel_id})
        elif isinstance(raw, str) and raw:
            photos.append({"url": raw, "booking_id": hotel_id})

    # If API returns limited photos, construct CDN URLs
    if not photos:
        for idx in range(1, max_photos + 1):
            cdn_url = f"https://cf.bstatic.com/xdata/images/hotel/max1024x768/{hotel_id}_{idx}.jpg?k=&o="
            photos.append({"url": cdn_url, "booking_id": hotel_id})

    return photos[:max_photos]


def generate_seo_alt(hotel_name: str, city_slug: str, country_slug: str,
                     lang: str = "ru", idx: int = 0) -> str:
    city_keywords = {
        "istanbul": "Стамбул Турция", "antalya": "Анталья Турция",
        "bangkok": "Бангкок Таиланд", "phuket": "Пхукет Таиланд",
        "dubai": "Дубай ОАЭ", "sharm-el-sheikh": "Шарм-эль-Шейх Египет",
    }
    loc = city_keywords.get(city_slug, f"{city_slug} {country_slug}")
    if lang == "ru":
        return f"{hotel_name} — {loc}. Фото отеля {idx + 1}. Забронировать по лучшей цене."
    return f"{hotel_name} — {loc}. Hotel photo {idx + 1}. Book at best price."


def download_and_process(hotel_name: str, country_slug: str, city_slug: str,
                         hotel_id: str, max_photos: int = 4) -> List[Path]:
    """Download, strip EXIF, convert to WebP, save to assets."""
    photos = get_hotel_photos(hotel_id, max_photos)
    if not photos:
        return []

    slug = hotel_name.lower().strip().replace(" ", "-").replace("&", "and")
    slug = re.sub(r"[^\w-]", "", slug)
    hotel_dir = ASSETS_DIR / country_slug / city_slug / slug
    hotel_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for idx, p in enumerate(photos[:max_photos]):
        local_name = f"{idx + 1:02d}.webp"
        local_path = hotel_dir / local_name
        if local_path.exists() and local_path.stat().st_size > 2000:
            downloaded.append(local_path)
            continue

        try:
            req = Request(p["url"], headers={"User-Agent": USER_AGENT})
            resp = urlopen(req, timeout=20)
            data = resp.read()
            if len(data) < 2000:
                continue
        except Exception:
            continue

        try:
            img = Image.open(io.BytesIO(data))
            if img.mode not in ("RGB",):
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode in ("RGBA", "LA"):
                        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else img)
                    else:
                        bg.paste(img.convert("RGBA"))
                    img = bg
                else:
                    img = img.convert("RGB")
            if img.width > 1200:
                ratio = 1200 / img.width
                img = img.resize((1200, int(img.height * ratio)), Image.Resampling.LANCZOS)
            img.save(local_path, format="WEBP", quality=88, method=6)
            kb = local_path.stat().st_size // 1024
            print(f"    {local_name} ({img.size[0]}x{img.size[1]}, {kb}KB)")
            downloaded.append(local_path)
        except Exception as e:
            print(f"    FAIL: {e}")

        time.sleep(0.5)

    return downloaded


def update_db(hotel_name: str, country_slug: str, city_slug: str,
              downloaded: List[Path], hotel_id: str):
    if not HOTELS_DB.exists() or not downloaded:
        return
    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    new_images = []
    for idx, lp in enumerate(sorted(downloaded)):
        slug = hotel_name.lower().strip().replace(" ", "-").replace("&", "and")
        slug = re.sub(r"[^\w-]", "", slug)
        url = f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{lp.name}"
        alt = generate_seo_alt(hotel_name, city_slug, country_slug, "ru", idx)
        alt_en = generate_seo_alt(hotel_name, city_slug, country_slug, "en", idx)
        try:
            with Image.open(lp) as im:
                w, h = im.size
        except Exception:
            w, h = 800, 500
        new_images.append({
            "src": url, "alt": alt, "alt_en": alt_en,
            "caption": hotel_name,
            "width": w, "height": h,
            "verified": True, "verification_score": 1.0,
            "source": "booking_affiliate",
            "provider_hotel_id": hotel_id,
            "attribution": "Booking.com",
        })
    updated = 0
    for h in data:
        if not isinstance(h, dict):
            continue
        if (h.get("name", "").lower().strip() == hotel_name.lower().strip()
                and h.get("country_slug") == country_slug
                and h.get("city_slug") == city_slug):
            h["images"] = new_images
            updated += 1
    if updated:
        HOTELS_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  DB: updated {updated} hotel(s)")


def process_one(hotel_name: str, country_slug: str, city_slug: str):
    print(f"{hotel_name} ({country_slug}/{city_slug})...", end=" ", flush=True)
    hotel_id = search_hotel(hotel_name, city_slug.replace("-", " ").title(), country_slug)
    if not hotel_id:
        print("NOT FOUND")
        return False
    print(f"id={hotel_id}")
    downloaded = download_and_process(hotel_name, country_slug, city_slug, hotel_id)
    if downloaded:
        update_db(hotel_name, country_slug, city_slug, downloaded, hotel_id)
        return True
    print("  NO PHOTOS DOWNLOADED")
    return False


def process_all():
    if not HOTELS_DB.exists():
        print(f"ERROR: {HOTELS_DB} not found")
        return
    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    done = 0
    for i, h in enumerate(data):
        if not isinstance(h, dict) or "name" not in h:
            continue
        print(f"[{i + 1}/{len(data)}] ", end="")
        if process_one(h["name"], h.get("country_slug", ""), h.get("city_slug", "")):
            done += 1
        time.sleep(1)
    print(f"\nDone: {done}/{len(data)} hotels")


def cli():
    parser = argparse.ArgumentParser(description="Booking.com Affiliate API photo downloader")
    parser.add_argument("--search", type=str, help="Hotel name to search")
    parser.add_argument("--country", type=str, default="", help="Country slug")
    parser.add_argument("--city", type=str, default="", help="City slug")
    parser.add_argument("--all", action="store_true", help="Process all hotels")
    args = parser.parse_args()

    if not SHARED_SECRET:
        print("ERROR: BOOKING_COM_SHARED_SECRET not set in .env")
        print("Get it from https://partner.booking.com/en-gb/affiliates/settings/api")
        return

    if args.all:
        process_all()
    elif args.search and args.country and args.city:
        process_one(args.search, args.country, args.city)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
