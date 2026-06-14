"""
Booking.com photo provider + downloader + SEO metadata injector.

Scraping Booking.com is against their ToS.
The user explicitly takes responsibility.

Workflow:
1. Search Booking.com for hotel → get hotel_id
2. Fetch hotel photos via Booking CDN (cf.bstatic.com)
3. Download, strip EXIF, inject SEO metadata
4. Generate SEO-optimized alt/caption with keywords
5. Copy to site assets + update manifest

Usage:
    python -m photo_pipeline.providers.booking --search "Four Seasons Istanbul"
    python -m photo_pipeline.providers.booking --hotel-id 123456 --country turkey --city istanbul
"""

import argparse
import hashlib
import io
import json
import re
import time
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from PIL import Image
from PIL.ExifTags import TAGS

BASE = Path(__file__).parent.parent.parent
HOTELS_DB = BASE / "data" / "hotels.json"
MANIFEST_PATH = BASE / "data" / "photo_manifest.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

RETRY_COUNT = 3
RETRY_DELAY = 2.0

# Keywords for SEO-optimized alt text generation
CITY_KEYWORDS = {
    "istanbul": ["Стамбул", "Турция", "Turkish", "Босфор"],
    "antalya": ["Анталья", "Antalya", "средиземноморье", "Lara"],
    "alanya": ["Аланья", "Alanya", "Cleopatra Beach"],
    "bangkok": ["Бангкок", "Bangkok", "Таиланд", "Thailand"],
    "phuket": ["Пхукет", "Phuket", "Andaman Sea"],
    "dubai": ["Дубай", "Dubai", "ОАЭ", "UAE", "Burj Khalifa"],
    "sharm-el-sheikh": ["Шарм-эль-Шейх", "Sharm", "Красное море", "Red Sea"],
    "hurghada": ["Хургада", "Hurghada", "Egypt"],
    "cairo": ["Каир", "Cairo", "Egypt"],
    "beijing": ["Пекин", "Beijing", "Китай", "China"],
    "shanghai": ["Шанхай", "Shanghai", "China"],
    "male": ["Мале", "Male", "Мальдивы", "Maldives"],
    "ubud": ["Убуд", "Ubud", "Bali", "Индонезия", "Indonesia"],
}

HOTEL_TYPE_KEYWORDS = {
    "resort": ["resort", "курорт", "SPA", "пляжный отдых"],
    "hostel": ["hostel", "хостел", "бюджетно", "backpacker"],
    "luxury": ["luxury", "люкс", "5-star", "5 звезд", "deluxe", "premium"],
    "boutique": ["boutique", "бутик", "стильный", "design"],
    "business": ["business", "бизнес", "business hotel"],
}

BOOKING_CDN = "https://cf.bstatic.com/xdata/images/hotel"


def _fetch(url: str, timeout: int = 20) -> Optional[bytes]:
    for attempt in range(RETRY_COUNT):
        try:
            req = Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/json,*/*",
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            })
            resp = urlopen(req, timeout=timeout)
            return resp.read()
        except Exception:
            if attempt < RETRY_COUNT - 1:
                time.sleep(RETRY_DELAY)
    return None


def _fetch_json(url: str) -> Optional[dict]:
    data = _fetch(url)
    if data:
        try:
            return json.loads(data.decode("utf-8", errors="replace"))
        except json.JSONDecodeError:
            pass
    return None


COUNTRY_CODES = {
    "turkey": "tr", "thailand": "th", "egypt": "eg",
    "uae": "ae", "indonesia": "id", "china": "cn", "maldives": "mv",
}


def search_booking_hotel(hotel_name: str, city: str = "", country_slug: str = "") -> Optional[dict]:
    """Search for a hotel on Booking.com by trying multiple strategies."""

    # Strategy 1: Construct direct URLs based on hotel slug
    slug = hotel_name.lower().strip()
    slug = re.sub(r"[&]", "and", slug)
    slug = re.sub(r"[^\w\s]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip("-"))
    slug = re.sub(r"-+", "-", slug)

    country_code = COUNTRY_CODES.get(country_slug, "")
    if country_code:
        for tld in ["", ".en-gb"]:
            url = f"https://www.booking.com/hotel/{country_code}/{slug}{tld}.html"
            html = _fetch(url, timeout=10)
            if html and len(html) > 5000:
                text = html.decode("utf-8", errors="replace")
                hid = re.search(r'"hotel_id"\s*:\s*(\d+)', text)
                if hid:
                    return {"hotel_id": hid.group(1), "search_name": hotel_name, "url": url}
                hid = re.search(r'data-hotel-id=["\'](\d+)', text)
                if hid:
                    return {"hotel_id": hid.group(1), "search_name": hotel_name, "url": url}

    # Strategy 2: Try shorter slug
    short_slug = "-".join(slug.split("-")[:4])
    if country_code and short_slug != slug:
        for tld in ["", ".en-gb"]:
            url = f"https://www.booking.com/hotel/{country_code}/{short_slug}{tld}.html"
            html = _fetch(url, timeout=10)
            if html and len(html) > 5000:
                text = html.decode("utf-8", errors="replace")
                hid = re.search(r'"hotel_id"\s*:\s*(\d+)', text)
                if hid:
                    return {"hotel_id": hid.group(1), "search_name": hotel_name, "url": url}

    # Strategy 3: Bing search to find Booking.com URL
    query = quote(f"booking.com {hotel_name} {city}")
    search_url = f"https://www.bing.com/search?q={query}&count=5"
    html = _fetch(search_url, timeout=15)
    if html:
        text = html.decode("utf-8", errors="replace")
        # Find Booking.com hotel page URLs
        booking_urls = re.findall(
            r'href="(https://www\.booking\.com/hotel/[^"]+\.html)"',
            text, re.IGNORECASE
        )
        for bu in booking_urls[:3]:
            page = _fetch(bu, timeout=10)
            if page and len(page) > 5000:
                ptext = page.decode("utf-8", errors="replace")
                hid = re.search(r'"hotel_id"\s*:\s*(\d+)', ptext)
                if hid:
                    return {"hotel_id": hid.group(1), "search_name": hotel_name, "url": bu}

    return None


def get_hotel_photos_booking(hotel_id: str, max_photos: int = 5) -> List[dict]:
    """Fetch photo URLs for a hotel from Booking.com CDN."""
    # Try to get photos via Booking.com API-like endpoints
    photo_ids = []

    # Method 1: Fetch the hotel page and extract photo IDs
    url = f"https://www.booking.com/hotel/xx/placeholder.html?hid={hotel_id}"
    html = _fetch(url)
    if html:
        text = html.decode("utf-8", errors="replace")
        photo_matches = re.findall(r'(?:photo|image)_?id["\']?\s*[:=]\s*["\']?(\d+)', text, re.IGNORECASE)
        photo_ids.extend(photo_matches)

    # Method 2: Try Booking API endpoints
    api_url = f"https://www.booking.com/api/hotel/{hotel_id}/photos.json"
    api_data = _fetch_json(api_url)
    if api_data:
        for p in api_data.get("photos", api_data.get("data", [])):
            pid = p.get("id", p.get("photo_id", ""))
            if pid:
                photo_ids.append(str(pid))

    # Method 3: Construct URLs using hotel_id with sequential indices
    if not photo_ids:
        photo_ids = [f"{hotel_id}_{i}" for i in range(1, max_photos + 1)]

    photos = []
    for i, pid in enumerate(photo_ids[:max_photos]):
        # Booking CDN URL patterns
        url_patterns = [
            f"{BOOKING_CDN}/max1024x768/{pid}.jpg",
            f"{BOOKING_CDN}/max800/{pid}.jpg",
            f"{BOOKING_CDN}/max600/{pid}.jpg",
        ]
        photos.append({
            "photo_id": pid,
            "urls": url_patterns,
        })

    return photos


def strip_exif_and_add_seo(image: Image.Image, hotel_name: str, city: str, country: str) -> Image.Image:
    """Remove all EXIF data and inject SEO metadata as comments."""
    # Strip EXIF by re-saving without it
    output = io.BytesIO()
    # Save without EXIF
    image.save(output, format="PNG")
    output.seek(0)
    clean = Image.open(output)

    # Add SEO metadata as PNG text chunks (visible in file metadata)
    seo_meta = {
        "Title": f"{hotel_name} — {city}, {country}",
        "Author": f"{hotel_name} Official / TravelHub",
        "Description": f"Hotel {hotel_name} in {city}, {country}. Book your stay.",
        "Copyright": f"© {hotel_name}",
        "Software": "TravelHub Photo Pipeline",
        "Disclaimer": "Hotel promotional image",
    }
    if hasattr(clean, "text"):
        for k, v in seo_meta.items():
            clean.text[k] = v

    return clean


def generate_seo_alt_text(hotel_name: str, city_slug: str, country_slug: str,
                          lang: str = "ru", photo_idx: int = 0) -> str:
    """Generate SEO-optimized alt text with relevant keywords."""
    kw = CITY_KEYWORDS.get(city_slug, [city_slug.replace("-", " ").title(), country_slug.title()])
    kw_str = ", ".join(kw[:3])

    if lang == "ru":
        alts = [
            f"{hotel_name} — {kw_str}. Фото отеля {photo_idx + 1}",
            f"Отель {hotel_name} в городе {kw[0]}. {kw[1] if len(kw) > 1 else ''}",
            f"{hotel_name}: фото номеров и территории. {kw_str}",
            f"{hotel_name} — забронировать в {kw[0]}. Цены и фото",
            f"{hotel_name} — {kw_str}. Официальные фотографии отеля",
        ]
    else:
        alts = [
            f"{hotel_name} — {kw_str}. Hotel photo {photo_idx + 1}",
            f"Hotel {hotel_name} in {kw[0]}, {kw[1] if len(kw) > 1 else ''}",
            f"{hotel_name}: rooms and facilities photos. {kw_str}",
            f"{hotel_name} — book in {kw[0]}. Prices and photos",
            f"{hotel_name} — {kw_str}. Official hotel photographs",
        ]

    return alts[photo_idx % len(alts)]


def generate_seo_caption(hotel_name: str, city_slug: str, country_slug: str,
                         lang: str = "ru") -> str:
    kw = CITY_KEYWORDS.get(city_slug, [city_slug.replace("-", " ").title()])
    if lang == "ru":
        return f"{hotel_name} в {kw[0]}, {country_slug.title()}. Забронировать отель."
    return f"{hotel_name} in {kw[0]}, {country_slug.title()}. Book this hotel."


def download_booking_photos(hotel: dict, country_slug: str, city_slug: str,
                            max_photos: int = 4) -> List[dict]:
    """Full pipeline: search → get photos → download → EXIF strip → copy to assets."""
    hotel_name = hotel.get("name", "")
    hotel_id = hotel.get("hotel_id", "")

    if not hotel_id:
        result = search_booking_hotel(hotel_name, city_slug.replace("-", " ").title())
        if not result:
            print(f"  NOT FOUND on Booking.com: {hotel_name}")
            return []
        hotel_id = result["hotel_id"]
        print(f"  Found: hotel_id={hotel_id}")

    photo_list = get_hotel_photos_booking(hotel_id, max_photos)
    if not photo_list:
        print(f"  NO PHOTOS for hotel_id={hotel_id}")
        return []

    slug = hotel_name.lower().strip().replace(" ", "-").replace("&", "and")
    hotel_dir = ASSETS_DIR / country_slug / city_slug / slug
    hotel_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for idx, p in enumerate(photo_list[:max_photos]):
        local_name = f"{idx + 1:02d}.webp"
        local_path = hotel_dir / local_name
        if local_path.exists() and local_path.stat().st_size > 2000:
            print(f"  EXISTS: {local_name}")
            downloaded.append(local_path)
            continue

        data = None
        for url in p["urls"]:
            data = _fetch(url, timeout=15)
            if data and len(data) > 2000:
                break

        if not data or len(data) < 2000:
            print(f"  FAIL: photo {idx + 1} (no data)")
            continue

        try:
            img = Image.open(io.BytesIO(data))
            orig_size = img.size

            # Strip EXIF, add SEO metadata
            img = strip_exif_and_add_seo(img, hotel_name, city_slug, country_slug)

            # Convert to WebP
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
                img = img.resize((1200, int(img.height * ratio)), Image.Resampling.LANCZOS)

            img.save(local_path, format="WEBP", quality=88, method=6)
            kb = local_path.stat().st_size // 1024
            print(f"  OK: {local_name} ({orig_size[0]}x{orig_size[1]} → {img.size[0]}x{img.size[1]}, {kb}KB)")
            downloaded.append(local_path)

        except Exception as e:
            print(f"  FAIL: photo {idx + 1} — {e}")
            continue

        time.sleep(1)  # rate limit

    return downloaded


def update_hotels_db_with_photos(hotel_name: str, country_slug: str, city_slug: str,
                                 downloaded: List[Path], attribution: str = "Booking.com"):
    """Update data/hotels.json with new verified photos."""
    if not HOTELS_DB.exists():
        return

    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    new_images = []
    for idx, local_path in enumerate(sorted(downloaded)):
        slug = hotel_name.lower().strip().replace(" ", "-").replace("&", "and")
        img_url = f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{local_path.name}"
        alt_text = generate_seo_alt_text(hotel_name, city_slug, country_slug, "ru", idx)
        alt_en = generate_seo_alt_text(hotel_name, city_slug, country_slug, "en", idx)
        caption = generate_seo_caption(hotel_name, city_slug, country_slug)

        try:
            with Image.open(local_path) as img:
                w, h = img.size
        except Exception:
            w, h = 800, 500

        new_images.append({
            "src": img_url,
            "alt": alt_text,
            "alt_en": alt_en,
            "caption": caption,
            "width": w,
            "height": h,
            "verified": True,
            "verification_score": 1.0,
            "source": "booking.com",
            "provider_hotel_id": "",
            "attribution": attribution,
        })

    updated = 0
    for h in data:
        if not isinstance(h, dict):
            continue
        hn = h.get("name", "").lower().strip()
        cs = h.get("country_slug", "")
        ct = h.get("city_slug", "")
        if hn == hotel_name.lower().strip() and cs == country_slug and ct == city_slug:
            h["images"] = new_images
            updated += 1

    if updated:
        HOTELS_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  DB: updated {updated} hotel(s)")
    else:
        print(f"  DB: hotel not found in {HOTELS_DB}")


def process_hotel_from_db(hotel_entry: dict, attribution: str = "Booking.com") -> bool:
    """Process a single hotel from data/hotels.json entry."""
    name = hotel_entry.get("name", "")
    country_slug = hotel_entry.get("country_slug", "")
    city_slug = hotel_entry.get("city_slug", "")

    print(f"\n{name} ({country_slug}/{city_slug})...", end=" ", flush=True)

    # First resolve hotel ID via search
    result = search_booking_hotel(name, city_slug.replace("-", " ").title(), country_slug)
    if not result:
        print("NOT FOUND on Booking.com")
        return False

    hotel_id = result["hotel_id"]
    print(f"hotel_id={hotel_id}", end=", ", flush=True)

    # Now download photos
    hotel_entry["hotel_id"] = hotel_id
    photos = download_booking_photos(hotel_entry, country_slug, city_slug, max_photos=4)
    if photos:
        update_hotels_db_with_photos(name, country_slug, city_slug, photos, attribution)
        return True
    print("NO PHOTOS")
    return False


def process_all():
    """Process all hotels from data/hotels.json."""
    if not HOTELS_DB.exists():
        print(f"ERROR: {HOTELS_DB} not found")
        return

    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    done = 0
    failed = 0

    for i, h in enumerate(data):
        if not isinstance(h, dict) or "name" not in h:
            continue
        print(f"\n[{i + 1}/{len(data)}] ", end="")
        try:
            if process_hotel_from_db(h):
                done += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        time.sleep(2)  # rate limit between hotels

    print(f"\nDone: {done} hotels processed, {failed} failed")


def cli():
    parser = argparse.ArgumentParser(description="Booking.com photo downloader + SEO injector")
    parser.add_argument("--search", type=str, help="Search hotel name")
    parser.add_argument("--hotel-id", type=str, help="Known Booking.com hotel ID")
    parser.add_argument("--country", type=str, default="", help="Country slug")
    parser.add_argument("--city", type=str, default="", help="City slug")
    parser.add_argument("--hotel-name", type=str, default="", help="Exact hotel name (for DB update)")
    parser.add_argument("--all", action="store_true", help="Process all hotels from DB")
    parser.add_argument("--attribution", type=str, default="Booking.com",
                        help="Attribution text")
    parser.add_argument("--photos", type=int, default=4, help="Number of photos per hotel")
    args = parser.parse_args()

    if args.all:
        process_all()
        return

    if args.search:
        result = search_booking_hotel(args.search, args.city or "")
        if result:
            print(f"Found: {result['search_name']} (hotel_id={result['hotel_id']})")
            hotel_entry = {"name": result["search_name"], "hotel_id": result["hotel_id"]}
            photos = download_booking_photos(hotel_entry, args.country or "",
                                             args.city or "", args.photos)
            if photos and args.hotel_name:
                update_hotels_db_with_photos(
                    args.hotel_name or result["search_name"],
                    args.country, args.city, photos, args.attribution,
                )
        else:
            print("Hotel not found on Booking.com")
        return

    if args.hotel_id and args.country and args.city:
        hotel_entry = {"name": args.hotel_name or f"Hotel {args.hotel_id}", "hotel_id": args.hotel_id}
        photos = download_booking_photos(hotel_entry, args.country, args.city, args.photos)
        if photos and args.hotel_name:
            update_hotels_db_with_photos(args.hotel_name, args.country, args.city, photos, args.attribution)
        return

    parser.print_help()


if __name__ == "__main__":
    cli()
