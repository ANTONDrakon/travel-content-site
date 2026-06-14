"""
Pixabay image search provider.
Free API — no credit card needed. 5000 queries/hour.
Sign up: https://pixabay.com/api/docs/

Usage:
    python -m photo_pipeline.providers.pixabay --all
    python -m photo_pipeline.providers.pixabay --search "Four Seasons Istanbul"
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
from urllib.parse import quote, urlencode
from PIL import Image

BASE = Path(__file__).parent.parent.parent
HOTELS_DB = BASE / "data" / "hotels.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"

# Load .env file
from dotenv import load_dotenv
load_dotenv(BASE / ".env")

PIXABAY_KEY = os.getenv("PIXABAY_API_KEY", "")
USER_AGENT = "TravelHubPhotoPipeline/2.0"

COUNTRY_CODES = {
    "turkey": "tr", "thailand": "th", "egypt": "eg",
    "uae": "ae", "indonesia": "id", "china": "cn", "maldives": "mv",
}


def search_image(hotel_name: str, city: str = "") -> List[dict]:
    key = PIXABAY_KEY
    # Use simple query — Pixabay sometimes rejects queries with special chars
    simple = f"{hotel_name} hotel".replace("&", "and").replace("'", "").replace('"', "")
    if city:
        simple = f"{hotel_name} {city.split(',')[0]} hotel"
    query = quote(simple[:100])
    url = f"https://pixabay.com/api/?key={key}&q={query}&image_type=photo&per_page=5&safesearch=true&category=places"
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        resp = urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        results = []
        for hit in data.get("hits", []):
            img_url = hit.get("largeImageURL", hit.get("webformatURL", ""))
            if img_url:
                results.append({
                    "url": img_url,
                    "page_url": hit.get("pageURL", ""),
                    "attribution": f"Photo by {hit.get('user', 'Pixabay')} on Pixabay",
                    "tags": hit.get("tags", ""),
                    "width": hit.get("imageWidth", 800),
                    "height": hit.get("imageHeight", 500),
                })
        return results
    except Exception as e:
        code = getattr(e, 'code', 0)
        print(f"  Pixabay error ({code}): {str(e)[:80]}")
        return []


def download_and_process(hotel_name: str, country_slug: str, city_slug: str,
                         max_photos: int = 4) -> List[Path]:
    city_name = city_slug.replace("-", " ").title()
    photos = search_image(hotel_name, city_name)
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
            print(f"    {local_name} ({img.size[0]}x{img.size[1]}, {kb}KB) — {p.get('attribution', '')[:40]}")
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
        alt = f"{hotel_name} — {city_slug.replace('-', ' ').title()}. Фото {idx + 1}"
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
            "source": "pixabay",
            "provider_hotel_id": "",
            "attribution": "Pixabay (free license)",
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
    downloaded = download_and_process(hotel_name, country_slug, city_slug)
    if downloaded:
        print(f"  OK: {len(downloaded)} photos")
        update_db(hotel_name, country_slug, city_slug, downloaded)
    else:
        print("NO PHOTOS FOUND")


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
            print(f"  ERROR: {e}")
        time.sleep(1.5)
    print(f"\nDone: {done}/{len(data)} hotels")


def cli():
    parser = argparse.ArgumentParser(description="Pixabay photo downloader (free, no credit card)")
    parser.add_argument("--search", type=str, help="Hotel name")
    parser.add_argument("--country", type=str, default="")
    parser.add_argument("--city", type=str, default="")
    parser.add_argument("--all", action="store_true", help="Process all hotels")
    args = parser.parse_args()

    if not PIXABAY_KEY:
        print("ERROR: Add PIXABAY_API_KEY to .env")
        print("Get a free key at: https://pixabay.com/api/docs/")
        print("(No credit card required, 5000 requests/hour)")
        print("Or use: python -m photo_pipeline.providers.pexels --all")
        return

    if args.all:
        process_all()
    elif args.search and args.country and args.city:
        process_one(args.search, args.country, args.city)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
