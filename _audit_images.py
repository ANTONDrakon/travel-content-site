"""Audit hotel photos and destination images for duplicates and mismatches."""
import json
from pathlib import Path

BASE = Path(__file__).parent
hotels = json.loads((BASE / "data" / "hotels.json").read_text(encoding="utf-8"))

# 1. Check which Unsplash photos are reused across hotels
photo_usage = {}  # url -> list of hotel names
for h in hotels:
    for img in h.get("images", []):
        src = img.get("src", "")
        # Check if this is a local file path (already downloaded)
        if src.startswith("/assets/hotels/"):
            continue
        if src not in photo_usage:
            photo_usage[src] = []
        photo_usage[src].append(h["name"])

print("=== DUPLICATE PHOTO URLs ===")
dups = {url: names for url, names in photo_usage.items() if len(names) > 1}
if dups:
    for url, names in sorted(dups.items(), key=lambda x: -len(x[1])):
        print(f"\n  Used by {len(names)} hotels:")
        for n in names[:5]:
            print(f"    - {n}")
        if len(names) > 5:
            print(f"    ... and {len(names)-5} more")
else:
    print("  None found - all photos are unique local files")

# 2. Check hotel photo files exist on disk
ASSETS = BASE / "docs" / "assets" / "hotels"
missing_photos = []
total_photos = 0
for h in hotels:
    slug = h["slug"]
    country = h["country_slug"]
    city = h["city_slug"]
    hotel_dir = ASSETS / country / city / slug
    if not hotel_dir.exists():
        missing_photos.append(f"{country}/{city}/{slug} (DIR MISSING)")
        continue
    files = list(hotel_dir.glob("*.webp"))
    total_photos += len(files)
    if len(files) < 3:
        missing_photos.append(f"{country}/{city}/{slug}: only {len(files)} photos")

print(f"\n=== HOTEL PHOTO STATS ===")
print(f"  Total hotels: {len(hotels)}")
print(f"  Total photo files: {total_photos}")
print(f"  Hotels with <3 photos: {len(missing_photos)}")
if missing_photos:
    for m in missing_photos[:20]:
        print(f"    {m}")

# 3. Check category distribution
cats = {}
for h in hotels:
    c = h.get("category", "unknown")
    cats[c] = cats.get(c, 0) + 1
print(f"\n=== CATEGORIES ===")
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")

# 4. Check verified vs unverified
verified = sum(1 for h in hotels if any(img.get("verified") for img in h.get("images", [])))
unverified = len(hotels) - verified
print(f"\n=== VERIFICATION ===")
print(f"  Verified: {verified}")
print(f"  Unverified: {unverified}")
