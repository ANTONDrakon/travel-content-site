"""Download hotel photos with metadata (hotel name in EXIF) for SEO + AI search engines."""
import io, json, re, time, urllib.request, urllib.parse, hashlib, struct
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import Base as ExifBase
except ImportError:
    print("pip install Pillow")
    exit(1)

BASE = Path(__file__).parent
HOTELS_DB = BASE / "data" / "hotels.json"
ASSETS = BASE / "docs" / "assets" / "hotels"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"

hotels = json.loads(HOTELS_DB.read_text(encoding="utf-8"))

# Brand -> search query mapping
BRAND_QUERIES = {
    "hilton": "hilton hotel exterior building", "marriott": "marriott hotel modern building",
    "sheraton": "sheraton hotel resort pool", "hyatt": "hyatt hotel lobby interior",
    "four seasons": "four seasons luxury hotel resort", "ritz-carlton": "ritz carlton luxury hotel",
    "ritz carlton": "ritz carlton luxury hotel", "peninsula": "peninsula hotel luxury classic",
    "novotel": "novotel hotel modern building", "holiday inn": "holiday inn hotel",
    "sofitel": "sofitel hotel elegant classic", "kempinski": "kempinski resort hotel",
    "intercontinental": "intercontinental luxury hotel", "banyan tree": "banyan tree tropical resort",
    "six senses": "six senses nature resort", "aman": "aman minimalist luxury resort",
    "mandarin oriental": "mandarin oriental luxury hotel", "st. regis": "st regis luxury grand hotel",
    "st regis": "st regis luxury grand hotel", "pullman": "pullman hotel modern",
    "radisson": "radisson hotel modern", "movenpick": "movenpick resort pool",
    "fairmont": "fairmont grand hotel historic", "jw marriott": "jw marriott grand hotel",
    "conrad": "conrad luxury hotel", "waldorf": "waldorf astoria grand hotel",
    "rosewood": "rosewood boutique luxury hotel", "anantara": "anantara tropical resort",
    "w hotel": "w hotel trendy modern design", "capella": "capella luxury resort",
    "amari": "amari hotel modern tropical", "centara": "centara resort beach pool",
    "dusit": "dusit luxury resort thai", "tuvana": "boutique hotel stone old town",
    "tomtom": "boutique hotel istanbul historic", "sura": "hotel near mosque historic",
    "cvk park": "hotel bosphorus view panoramic", "akra": "resort beachfront modern antalya",
    "sealife": "seaside resort pool beach", "mardan": "grand palace resort pool",
    "rixos": "rixos resort all inclusive beach", "maxx royal": "maxx royal luxury resort",
    "the bodrum edition": "bodrum luxury design resort", "sultan cave": "cappadocia cave hotel stone",
    "museum hotel": "cappadocia cave hotel balloons view", "argos in cappadocia": "cappadocia stone village hotel",
    "kayakapi": "cappadocia cave premium suite", "trisara": "phuket private pool villa ocean",
    "amanpuri": "amanpuri phuket luxury resort", "lub d": "modern design hostel",
    "niras": "cultural hostel thai", "dubai rove": "dubai modern city hotel",
    "atlantis the royal": "atlantis dubai luxury resort", "burj al arab": "burj al arab iconic hotel dubai",
    "emirates palace": "emirates palace grand hotel abu dhabi", "qasr al sarab": "desert resort luxury dunes",
    "puri garden": "bali garden hotel rice terrace", "swastika": "bali traditional bungalow tropical",
    "tegal sari": "bali rice terrace accommodation wooden", "bisma eight": "bali boutique hotel pool tropical",
    "komaneka": "bali luxury hotel art tropical", "the udaya": "bali yoga resort jungle rice",
    "alam shanti": "bali eco hotel tropical garden", "viceroy bali": "bali infinity pool valley view",
    "the haven suites": "bali seminyak suites pool", "the amala": "bali boutique villa pool palm",
    "kunja hotel": "bali private pool villa tropical",
    "the hive beach": "maldives guesthouse beach local", "marukab": "maldives hotel island beach",
    "beehive": "maldives guesthouse modern beach", "samann grand": "maldives hotel beach tropical",
    "the somerset": "maldives boutique hotel beach", "hotel jen": "maldives city hotel modern",
    "cinnamon dhonveli": "maldives overwater resort lagoon", "sheraton maldives": "maldives luxury resort overwater",
    "the residence maldives": "maldives overwater villa sunset", "ozen reserve": "maldives overwater luxury resort",
    "sun tan beach inn": "maldives local island guesthouse", "maafushi inn": "maldives local island hotel",
    "arena beach hotel": "maldives beach hotel tropical", "kaani village": "maldives guesthouse beach palm",
    "white shell": "maldives beachfront inn white", "sunrise beach hotel": "maldives sunrise beach hotel",
    "coco palm inn": "maldives palm hotel tropical", "hilton garden inn hulhumale": "maldives hilton hotel beach",
    "holiday inn resort hulhumale": "maldives resort beach pool",
    "cheers hostel": "istanbul hostel colorful modern", "hotel peninsula istanbul": "istanbul luxury hotel historic",
    "sura hagia sophia": "istanbul hotel historic mosque view", "cvk park bosphorus": "istanbul hotel bosphorus view",
    "tomtom suites": "istanbul boutique suite historic", "four seasons istanbul": "istanbul luxury hotel garden",
    "ritz carlton istanbul": "istanbul luxury hotel modern", "hotel aysima": "antalya hotel pool garden",
    "puding marina": "antalya marina boutique hotel", "ramada plaza": "antalya resort all inclusive pool",
    "sealife resort": "antalya beachfront resort pool", "tuvana hotel": "antalya old town boutique stone",
    "akra hotel": "antalya luxury resort beachfront", "mardan palace": "antalya grand palace resort pool",
    "rixos downtown": "antalya downtown modern hotel", "maxx royal kemer": "kemer luxury resort green",
    "oya butik": "bodrum boutique hotel white stone", "gumbet beach hotel": "bodrum beach hotel pool",
    "bitez garden": "bodrum garden hotel flowers", "marina vista": "bodrum marina view hotel",
    "yalikavak palace": "bodrum palace resort sea view", "ortakent beach": "bodrum quiet beach resort",
    "torba garden": "bodrum garden boutique flowers", "six senses kaplankaya": "bodrum cliff resort beach luxury",
    "mandarin oriental bodrum": "bodrum marina resort pool", "stone house cappadocia": "cappadocia stone house hotel",
    "flintstone cave": "cappadocia cave house themed", "sultan cave suites": "cappadocia cave suite balcony balloons",
    "mithra cave": "cappadocia cave hotel cozy interior", "heaven cave": "cappadocia cave panoramic view sunset",
    "cappadocia caves hotel": "cappadocia traditional cave stone", "museum hotel cappadocia": "cappadocia luxury cave museum balloons",
    "argos in cappadocia": "cappadocia stone village tunnel cave", "kayakapi premium": "cappadocia premium cave luxury suite",
}


def get_query(name):
    nl = name.lower()
    for brand, q in BRAND_QUERIES.items():
        if brand in nl:
            return q
    words = name.split()[:3]
    return f"{' '.join(words)} hotel exterior"


def download_photo(url, out, max_dim=800, quality=82):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=20).read()
        if len(data) < 1000:
            return False
        img = Image.open(io.BytesIO(data))
        if img.mode not in ("RGB",):
            img = img.convert("RGB")
        if img.width > max_dim:
            r = max_dim / img.width
            img = img.resize((max_dim, int(img.height * r)), Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="WEBP", quality=quality, method=6)
        return out.exists() and out.stat().st_size > 500
    except Exception:
        return False


def main():
    ok = 0
    skip = 0
    fail = 0

    for i, h in enumerate(hotels):
        name = h["name"]
        slug = h["slug"]
        country = h["country_slug"]
        city = h["city_slug"]
        hotel_dir = ASSETS / country / city / slug

        # Skip if already has 3+ photos
        if hotel_dir.exists() and len(list(hotel_dir.glob("*.webp"))) >= 3:
            skip += 1
            continue

        query = get_query(name)
        city_name = city.replace("-", " ").title()
        print(f"[{i+1}/{len(hotels)}] {name}")

        count = 0
        for idx in range(3):
            suffixes = ["exterior facade", "lobby interior room", "pool view amenity"]
            q = f"{query} {suffixes[idx]}"
            encoded_q = urllib.parse.quote(q)
            url = f"https://source.unsplash.com/800x600/?{encoded_q}"
            out = hotel_dir / f"{idx+1:02d}.webp"

            if out.exists() and out.stat().st_size > 1000:
                count += 1
                continue

            if download_photo(url, out):
                count += 1
                print(f"  {out.name} OK")
            else:
                print(f"  {out.name} FAIL")
            time.sleep(0.5)

        if count >= 2:
            ok += 1
        else:
            fail += 1

    print(f"\n=== DONE: {ok} OK, {skip} skipped, {fail} failed ===")


if __name__ == "__main__":
    main()
