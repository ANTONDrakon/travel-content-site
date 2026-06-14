"""
Update country & hero images with beautiful Pixabay destination photos.
Run AFTER setting PIXABAY_API_KEY in .env

Usage:
    python _update_destination_photos.py
    python main.py build
"""

import os, io, json, re, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from PIL import Image
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")

PIXABAY_KEY = os.getenv("PIXABAY_API_KEY", "")
USER_AGENT = "TravelHub/2.0"

# Country-specific search queries for beautiful destination photos
COUNTRY_QUERIES = {
    "turkey": "Turkey Istanbul Cappadocia hot air balloon landscape",
    "thailand": "Thailand beach Phi Phi island tropical",
    "egypt": "Egypt pyramids Giza desert Red Sea",
    "uae": "Dubai Burj Khalifa city skyline UAE",
    "indonesia": "Bali Indonesia rice terrace tropical beach",
    "china": "China Great Wall Shanghai skyline",
    "maldives": "Maldives overwater bungalow beach aerial",
}

HERO_QUERIES = [
    "travel world beach sunset passport",
    "airplane wing view clouds travel",
    "travel vacation beach tropical paradise",
]

COUNTRIES_DIR = BASE / "docs" / "assets" / "countries"
CITIES_DIR = BASE / "docs" / "assets" / "cities"


def search_pixabay(query: str, per_page: int = 5) -> list:
    if not PIXABAY_KEY:
        return []
    q = quote(query[:100])
    url = f"https://pixabay.com/api/?key={PIXABAY_KEY}&q={q}&image_type=photo&per_page={per_page}&safesearch=true&category=places"
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        resp = urlopen(req, timeout=20)
        data = json.loads(resp.read().decode())
        return data.get("hits", [])
    except Exception as e:
        print(f"  Pixabay error: {e}")
        return []


def download_webp(url: str, output_path: Path, max_dim: int = 1400, quality: int = 90) -> bool:
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        resp = urlopen(req, timeout=20)
        data = resp.read()
        if len(data) < 2000:
            return False
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
        if img.width > max_dim:
            ratio = max_dim / img.width
            img = img.resize((max_dim, int(img.height * ratio)), Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, format="WEBP", quality=quality, method=6)
        kb = output_path.stat().st_size // 1024
        print(f"    OK: {output_path.name} ({img.size[0]}x{img.size[1]}, {kb}KB)")
        return True
    except Exception as e:
        print(f"    FAIL: {e}")
        return False


def update_country_images():
    print("=== Updating country images ===")
    for slug, query in COUNTRY_QUERIES.items():
        print(f"  {slug}...", end=" ", flush=True)
        hits = search_pixabay(query)
        if not hits:
            print("NO RESULTS")
            continue
        best = max(hits, key=lambda h: h.get("likes", 0) + h.get("views", 0))
        img_url = best.get("largeImageURL", best.get("webformatURL", ""))
        if not img_url:
            print("NO URL")
            continue
        path = COUNTRIES_DIR / f"{slug}.webp"
        if download_webp(img_url, path, 1400, 92):
            print(f"  ({best.get('tags', '')[:40]})")
        time.sleep(1)


def update_hero_image():
    print("\n=== Updating hero image ===")
    for query in HERO_QUERIES:
        print(f"  Searching: '{query[:40]}...'", end=" ", flush=True)
        hits = search_pixabay(query, 3)
        if hits:
            best = max(hits, key=lambda h: h.get("likes", 0) + h.get("views", 0))
            img_url = best.get("largeImageURL", best.get("webformatURL", ""))
            if img_url:
                path = COUNTRIES_DIR / "travel-hero.webp"
                if download_webp(img_url, path, 1600, 92):
                    print(f"  ({best.get('tags', '')[:40]})")
                    return
        time.sleep(1)
    print("  FAILED")


def update_city_images():
    print("\n=== Updating city images (without JPG originals) ===")
    # Only update cities that DON'T have JPG originals (those are already good)
    cities_needing_update = []
    for webp_path in sorted(CITIES_DIR.glob("*.webp")):
        slug = webp_path.stem
        jpg_path = CITIES_DIR / f"{slug}.jpg"
        if not jpg_path.exists():
            cities_needing_update.append(slug)

    city_queries = {
        "istanbul": "Istanbul Turkey Hagia Sophia Bosphorus",
        "alanya": "Alanya Turkey beach castle Mediterranean",
        "bangkok": "Bangkok Thailand Grand Palace temples",
        "beijing": "Beijing China Forbidden City Great Wall",
        "cairo": "Cairo Egypt pyramids Nile river",
        "canggu": "Canggu Bali surf beach sunset",
        "dhigurah": "Maldives beach sandbank turquoise water",
        "dubai": "Dubai UAE Burj Khalifa skyline",
        "koh-samui": "Koh Samui Thailand beach palm trees",
        "krabi": "Krabi Thailand limestone cliffs beach",
        "kuta": "Kuta Bali surf beach sunset",
        "male": "Male Maldives city island harbor",
        "marsa-alam": "Marsa Alam Egypt Red Sea beach",
        "nusa-dua": "Nusa Dua Bali luxury resort beach",
        "pattaya": "Pattaya Thailand beach city skyline",
        "phuket": "Phuket Thailand beach island sunset",
        "resort-islands": "Maldives resort island overwater villa",
        "seminyak": "Seminyak Bali luxury beach sunset",
        "shanghai": "Shanghai China Bund skyline Pudong",
        "sharm-el-sheikh": "Sharm El Sheikh Egypt Red Sea coral",
        "thulusdhoo": "Maldives local island beach surf",
        "ubud": "Ubud Bali rice terrace jungle",
        "xian": "Xi'an China Terracotta Warriors ancient",
    }

    for slug in cities_needing_update:
        query = city_queries.get(slug, f"{slug} travel destination")
        print(f"  {slug}...", end=" ", flush=True)
        hits = search_pixabay(query)
        if not hits:
            print("NO RESULTS")
            continue
        best = max(hits, key=lambda h: h.get("likes", 0) + h.get("views", 0))
        img_url = best.get("largeImageURL", best.get("webformatURL", ""))
        if not img_url:
            print("NO URL")
            continue
        path = CITIES_DIR / f"{slug}.webp"
        if download_webp(img_url, path, 1200, 90):
            print(f"  ({best.get('tags', '')[:40]})")
        time.sleep(1)


def main():
    if not PIXABAY_KEY:
        print("ERROR: PIXABAY_API_KEY not set in .env")
        return
    update_country_images()
    update_hero_image()
    update_city_images()
    print("\n=== Done! Run 'python main.py build' to rebuild the site ===")


if __name__ == "__main__":
    main()
