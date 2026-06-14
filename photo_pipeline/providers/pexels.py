"""
Pexels photo provider — free API, no credit card needed.
Sign up: https://www.pexels.com/api/
Free tier: 200 requests/hour, 800 requests/day.

Usage:
    python -m photo_pipeline.providers.pexels --all
"""

import argparse
import io
import json
import os
import re
import time
from pathlib import Path
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.parse import quote
from PIL import Image

BASE = Path(__file__).parent.parent.parent
HOTELS_DB = BASE / "data" / "hotels.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"

PEXELS_KEY = os.getenv("PEXELS_API_KEY", "")
USER_AGENT = "TravelHubPhotoPipeline/2.0"


def search_pexels(hotel_name: str, city: str = "") -> List[dict]:
    if not PEXELS_KEY:
        return []

    # Build search query
    keywords = f"{hotel_name} {city} hotel".strip().replace("&", "and")
    keywords = keywords[:100]
    query = quote(keywords)

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=5&orientation=landscape"
    try:
        req = Request(url, headers={"Authorization": PEXELS_KEY, "User-Agent": USER_AGENT})
        resp = urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        results = []
        for photo in data.get("photos", []):
            src = photo.get("src", {})
            img_url = src.get("large2x") or src.get("large") or src.get("medium", "")
            if img_url:
                results.append({
                    "url": img_url,
                    "page_url": photo.get("url", ""),
                    "attribution": f"Photo by {photo.get('photographer', 'Pexels')} on Pexels",
                    "width": photo.get("width", 800),
                    "height": photo.get("height", 500),
                })
        return results
    except Exception as e:
        code = getattr(e, 'code', 0)
        print(f"  Pexels error ({code}): {str(e)[:80]}")
        return []


def download_and_process(hotel_name: str, country_slug: str, city_slug: str,
                         max_photos: int = 4) -> List[Path]:
    city_name = city_slug.replace("-", " ").title()
    photos = search_pexels(hotel_name, city_name)
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
            img.save(local_path, format="WEBP", quality=85, method=6)
            kb = local_path.stat().st_size // 1024
            print(f"    {local_name} ({img.size[0]}x{img.size[1]}, {kb}KB)")
            downloaded.append(local_path)
        except Exception as e:
            print(f"    FAIL: {e}")
        time.sleep(0.5)

    return downloaded


def update_db(hotel_name: str, country_slug: str, city_slug: str, downloaded: List[Path]):
    if not HOTELS_DB.exists() or not downloaded:
        return
    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    new_images = []
    for idx, lp in enumerate(sorted(downloaded)):
        slug = hotel_name.lower().strip().replace(" ", "-").replace("&", "and")
        slug = re.sub(r"[^\w-]", "", slug)
        url = f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{lp.name}"
        alt = f"{hotel_name} — {city_slug.replace('-', ' ').title()}. Фото отеля {idx + 1}"
        try:
            with Image.open(lp) as im:
                w, h = im.size
        except Exception:
            w, h = 800, 500
        new_images.append({
            "src": url, "alt": alt, "alt_en": alt,
            "caption": hotel_name,
            "width": w, "height": h,
            "verified": True, "verification_score": 1.0,
            "source": "pexels",
            "provider_hotel_id": "",
            "attribution": "Pexels (free license)",
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
    print(f"{hotel_name}...", end=" ", flush=True)
    downloaded = download_and_process(hotel_name, country_slug, city_slug)
    if downloaded:
        print(f"OK: {len(downloaded)} photos")
        update_db(hotel_name, country_slug, city_slug, downloaded)
    else:
        print("NO PHOTOS")


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
        try:
            process_one(h["name"], h.get("country_slug", ""), h.get("city_slug", ""))
            done += 1
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(1.5)
    print(f"\nDone: {done}/{len(data)} hotels")


def cli():
    parser = argparse.ArgumentParser(description="Pexels photo downloader (free, no CC)")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--search", type=str)
    parser.add_argument("--country", type=str, default="")
    parser.add_argument("--city", type=str, default="")
    args = parser.parse_args()

    if not PEXELS_KEY:
        print("ERROR: Add PEXELS_API_KEY to .env")
        print("Get a free key at: https://www.pexels.com/api/")
        print("(No credit card required, 200 free requests/hour)")
        return

    if args.all:
        process_all()
    elif args.search and args.country and args.city:
        process_one(args.search, args.country, args.city)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
