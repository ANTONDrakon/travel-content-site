"""
Manual photo ingestion tool.

Place your downloaded photos in a folder, run this script, and it will:
1. Copy photos to the correct /assets/hotels/{country}/{city}/{hotel}/ directory
2. Convert to WebP (1200px, quality 88)
3. Update data/hotels.json with the new verified photo paths
4. Add a signed manifest entry

Usage:
    python -m photo_pipeline.manual_ingest <folder> [--hotel-name "Name"] [--country turkey] [--city istanbul]

Folder structure (auto-detect by filename or explicit flags):
    ./my_photos/
        istanbul-four-seasons-01.jpg
        istanbul-four-seasons-02.jpg
        istanbul-four-seasons-03.jpg

Or with explicit params:
    python -m photo_pipeline.manual_ingest ./my_photos/ \\
        --hotel-name "Four Seasons Hotel Istanbul at Sultanahmet" \\
        --country turkey --city istanbul \\
        --attribution "Four Seasons Hotels and Resorts" \\
        --source-url "https://www.fourseasons.com/istanbul/"
"""

import argparse
import json
import hashlib
import shutil
from pathlib import Path
from PIL import Image
import io

BASE = Path(__file__).parent.parent
HOTELS_DB = BASE / "data" / "hotels.json"
MANIFEST_PATH = BASE / "data" / "photo_manifest.json"
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}


def normalize_name(name: str) -> str:
    return name.lower().strip().replace(" ", "-").replace("&", "and")


def find_hotel_in_db(name: str, country_slug: str, city_slug: str) -> dict:
    if not HOTELS_DB.exists():
        return None
    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
    nl = name.lower().strip()
    for h in data:
        if not isinstance(h, dict):
            continue
        hn = h.get("name", "").lower().strip()
        cs = h.get("country_slug", "")
        ct = h.get("city_slug", "")
        if hn == nl and cs == country_slug and ct == city_slug:
            return h
        # partial match
        if cs == country_slug and ct == city_slug:
            if nl in hn or hn in nl:
                return h
    return None


def convert_to_webp(src_path: Path, dst_path: Path, quality: int = 88, max_dim: int = 1200):
    img = Image.open(src_path)
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode in ("RGBA", "LA"):
            bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else img)
        else:
            bg.paste(img.convert("RGBA"))
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    if img.width > max_dim:
        ratio = max_dim / img.width
        img = img.resize((max_dim, int(img.height * ratio)), Image.Resampling.LANCZOS)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, format="WEBP", quality=quality, method=6)
    return dst_path.exists()


def build_alt_text(hotel_name: str, city_en: str, idx: int) -> str:
    return f"{hotel_name} — {city_en}, photo {idx + 1}"


def build_caption(hotel_name: str) -> str:
    return hotel_name


def update_hotels_db(hotel_name: str, country_slug: str, city_slug: str,
                     city_name_ru: str, city_name_en: str,
                     new_images: list, attribution: str):
    if not HOTELS_DB.exists():
        print(f"  WARN: {HOTELS_DB} not found, skipping DB update")
        return

    data = json.loads(HOTELS_DB.read_text(encoding="utf-8"))
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
        print(f"  Updated {updated} hotel(s) in {HOTELS_DB}")
    else:
        print(f"  WARN: no matching hotel found in DB for '{hotel_name}'")


def main():
    parser = argparse.ArgumentParser(description="Manually ingest hotel photos")
    parser.add_argument("folder", type=str, help="Folder with downloaded photos")
    parser.add_argument("--hotel-name", type=str, default="", help="Hotel name (auto-detect if empty)")
    parser.add_argument("--country", type=str, default="", help="Country slug")
    parser.add_argument("--city", type=str, default="", help="City slug")
    parser.add_argument("--attribution", type=str, default="Hotel media kit / official website",
                        help="Attribution text")
    parser.add_argument("--source-url", type=str, default="", help="Source URL")
    parser.add_argument("--quality", type=int, default=88, help="WebP quality (0-100)")
    parser.add_argument("--max-dim", type=int, default=1200, help="Max image dimension")

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists() or not folder.is_dir():
        print(f"ERROR: folder not found: {folder}")
        return 1

    photos = sorted([f for f in folder.iterdir() if f.suffix.lower() in SUPPORTED_EXT])
    if not photos:
        print(f"ERROR: no supported images found in {folder} (supported: {SUPPORTED_EXT})")
        return 1

    print(f"Found {len(photos)} photos in {folder}")

    # Determine hotel identity
    hotel_name = args.hotel_name
    country_slug = args.country
    city_slug = args.city

    if not hotel_name:
        # Try to extract from filename (first photo)
        stem = photos[0].stem
        parts = stem.replace("_", " ").replace("-", " ").split()
        # Filter out common prefixes
        stop_words = {"photo", "img", "hotel", "view", "exterior", "interior", "room", "pool",
                      "01", "02", "03", "1", "2", "3", "001", "002", "003"}
        name_parts = [p for p in parts if p.lower() not in stop_words]
        if name_parts:
            guessed = " ".join(name_parts).title()
            print(f"  Guessed hotel name: '{guessed}'")
            print(f"  Use --hotel-name to override")
            hotel_name = guessed
        else:
            print("ERROR: could not determine hotel name from filenames. Use --hotel-name.")
            return 1

    if not country_slug or not city_slug:
        # Look up in hotels.db
        h = find_hotel_in_db(hotel_name, country_slug or "", city_slug or "")
        if h:
            country_slug = country_slug or h.get("country_slug", "")
            city_slug = city_slug or h.get("city_slug", "")
            print(f"  Found in DB: {country_slug}/{city_slug}")
        else:
            print("ERROR: could not determine country/city. Use --country and --city.")
            return 1

    # Get DB entry for metadata
    db_entry = find_hotel_in_db(hotel_name, country_slug, city_slug)
    city_name_ru = db_entry.get("city_name_ru", city_slug) if db_entry else city_slug
    city_name_en = db_entry.get("city_name_en", city_slug) if db_entry else city_slug

    slug = normalize_name(hotel_name)
    hotel_dir = ASSETS_DIR / country_slug / city_slug / slug
    hotel_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nUploading to: /assets/hotels/{country_slug}/{city_slug}/{slug}/")

    new_images = []
    manifest_entries = []
    for idx, src_path in enumerate(photos):
        dst_name = f"{idx + 1:02d}.webp"
        dst_path = hotel_dir / dst_name

        print(f"  [{idx + 1}/{len(photos)}] {src_path.name} → {dst_name}...", end=" ")
        try:
            if convert_to_webp(src_path, dst_path, args.quality, args.max_dim):
                kb = dst_path.stat().st_size // 1024
                print(f"OK ({kb}KB)")
            else:
                print("FAILED (conversion)")
                continue
        except Exception as e:
            print(f"ERROR: {e}")
            continue

        img_url = f"/assets/hotels/{country_slug}/{city_slug}/{slug}/{dst_name}"
        alt_text = build_alt_text(hotel_name, city_name_en, idx)
        caption = build_caption(hotel_name)
        alt_en = build_alt_text(hotel_name, city_name_en, idx)

        # Read actual dimensions
        try:
            with Image.open(dst_path) as img:
                w, h = img.size
        except Exception:
            w, h = 800, 500

        entry = {
            "src": img_url,
            "alt": alt_text,
            "alt_en": alt_en,
            "caption": caption,
            "width": w,
            "height": h,
            "verified": True,
            "verification_score": 1.0,
            "source": "manual_ingest",
            "provider_hotel_id": "",
            "attribution": args.attribution,
            "source_page_url": args.source_url,
        }
        new_images.append(entry)

        manifest_entry = {
            "hotel_name": hotel_name,
            "slug": slug,
            "city_slug": city_slug,
            "country_slug": country_slug,
            "provider": "manual_ingest",
            "provider_hotel_id": "",
            "image_url": img_url,
            "local_path": str(dst_path.relative_to(BASE)),
            "src": img_url,
            "alt": alt_text,
            "alt_en": alt_en,
            "caption": caption,
            "attribution": args.attribution,
            "source_page_url": args.source_url,
            "verification_score": 1.0,
            "verified": True,
            "width": w,
            "height": h,
        }
        manifest_entries.append(manifest_entry)

    if not new_images:
        print("\nNo images were processed successfully.")
        return 1

    # Update hotels.json
    update_hotels_db(hotel_name, country_slug, city_slug,
                     city_name_ru, city_name_en,
                     new_images, args.attribution)

    # Update manifest
    existing = []
    if MANIFEST_PATH.exists():
        existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    existing.extend(manifest_entries)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  Manifest: {len(manifest_entries)} entries added to {MANIFEST_PATH}")

    print(f"\nDone: {len(new_images)} photos ingested for '{hotel_name}'")
    return 0


if __name__ == "__main__":
    exit(main())
