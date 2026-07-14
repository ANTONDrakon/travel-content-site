"""Download unique country and city images from Unsplash (free, no API key)."""
import io, os, time, urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    exit(1)

BASE = Path(__file__).parent
COUNTRIES_DIR = BASE / "docs" / "assets" / "countries"
CITIES_DIR = BASE / "docs" / "assets" / "cities"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"

# Country hero images - specific, beautiful, recognizable
COUNTRY_IMAGES = {
    "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1400&q=85",
    "thailand": "https://images.unsplash.com/photo-1528181304800-259b08848526?w=1400&q=85",
    "egypt": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1400&q=85",
    "uae": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1400&q=85",
    "indonesia": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1400&q=85",
    "china": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1400&q=85",
    "maldives": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1400&q=85",
}

# City images - unique per city
CITY_IMAGES = {
    # Turkey
    "istanbul": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=1000&q=85",
    "antalya": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1000&q=85",
    "bodrum": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1000&q=85",
    "cappadocia": "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?w=1000&q=85",
    # Thailand
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1000&q=85",
    "phuket": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=1000&q=85",
    "pattaya": "https://images.unsplash.com/photo-1506665531195-3566af2b4dfa?w=1000&q=85",
    "koh-samui": "https://images.unsplash.com/photo-1504681869696-d977211a5f4c?w=1000&q=85",
    "krabi": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1000&q=85",
    # Egypt
    "sharm-el-sheikh": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1000&q=85",
    "hurghada": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1000&q=85",
    "cairo": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1000&q=85",
    "luxor": "https://images.unsplash.com/photo-1568322445389-f64a1b72f7c5?w=1000&q=85",
    "marsa-alam": "https://images.unsplash.com/photo-1544551763-7266fa257723?w=1000&q=85",
    # UAE
    "dubai": "https://images.unsplash.com/photo-1518684079-3c830dcef090?w=1000&q=85",
    "abu-dhabi": "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=1000&q=85",
    "sharjah": "https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=1000&q=85",
    "ras-al-khaimah": "https://images.unsplash.com/photo-1597659840241-37e2b9c2f55f?w=1000&q=85",
    "fujairah": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=1000&q=85",
    # Indonesia
    "ubud": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1000&q=85",
    "kuta": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1000&q=85",
    "seminyak": "https://images.unsplash.com/photo-1573790387438-4da905039392?w=1000&q=85",
    "canggu": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1000&q=85",
    "nusa-dua": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=1000&q=85",
    # China
    "sanya": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1000&q=85",
    "haikou": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1000&q=85",
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1000&q=85",
    "shanghai": "https://images.unsplash.com/photo-1546412414-e1885e5109b5?w=1000&q=85",
    "xian": "https://images.unsplash.com/photo-1590736969955-71cc94901144?w=1000&q=85",
    # Maldives
    "male": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1000&q=85",
    "maafushi": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=1000&q=85",
    "hulhumale": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1000&q=85",
    "thulusdhoo": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1000&q=85",
    "dhigurah": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1000&q=85",
    "resort-islands": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1000&q=85",
}


def download_image(url, output_path, max_dim=1400, quality=88):
    """Download image from URL, convert to WebP."""
    if output_path.exists() and output_path.stat().st_size > 5000:
        print(f"  SKIP (exists): {output_path.name}")
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=20)
        data = resp.read()
        if len(data) < 2000:
            print(f"  FAIL (too small): {len(data)} bytes")
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
            img = img.resize((max_dim, int(img.height * ratio)), Image.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, format="WEBP", quality=quality, method=6)
        kb = output_path.stat().st_size // 1024
        print(f"  OK: {output_path.name} ({img.size[0]}x{img.size[1]}, {kb}KB)")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    print("=== Downloading country images ===")
    for slug, url in COUNTRY_IMAGES.items():
        out = COUNTRIES_DIR / f"{slug}.webp"
        print(f"  {slug}...", end=" ")
        download_image(url, out, 1400, 90)
        time.sleep(0.5)

    print("\n=== Downloading city images ===")
    for slug, url in CITY_IMAGES.items():
        out = CITIES_DIR / f"{slug}.webp"
        print(f"  {slug}...", end=" ")
        download_image(url, out, 1000, 88)
        time.sleep(0.5)

    print("\n=== Done! ===")
    print("Run 'python main.py build' to rebuild the site.")


if __name__ == "__main__":
    main()
