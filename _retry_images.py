"""Retry failed city images with alternative URLs."""
import io, time, urllib.request
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
CITIES_DIR = BASE / "docs" / "assets" / "cities"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"

# Alternative URLs for failed cities
RETRY_IMAGES = {
    "bangkok": "https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=1000&q=85",
    "koh-samui": "https://images.unsplash.com/photo-1506665531195-3566af2b4dfa?w=1000&q=85",
    "krabi": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1000&q=85",
    "cairo": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1000&q=85",
    "kuta": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1000&q=85",
    "seminyak": "https://images.unsplash.com/photo-1573790387438-4da905039392?w=1000&q=85",
    "canggu": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1000&q=85",
    "nusa-dua": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=1000&q=85",
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1000&q=85",
    "xian": "https://images.unsplash.com/photo-1590736969955-71cc94901144?w=1000&q=85",
    "male": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1000&q=85",
}

def download(url, out):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=25)
        data = resp.read()
        if len(data) < 2000:
            return False
        img = Image.open(io.BytesIO(data))
        if img.mode != "RGB":
            img = img.convert("RGB")
        if img.width > 1000:
            r = 1000 / img.width
            img = img.resize((1000, int(img.height * r)), Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="WEBP", quality=88, method=6)
        kb = out.stat().st_size // 1024
        print(f"  OK: {out.name} ({img.size[0]}x{img.size[1]}, {kb}KB)")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

for slug, url in RETRY_IMAGES.items():
    out = CITIES_DIR / f"{slug}.webp"
    if out.exists() and out.stat().st_size > 5000:
        print(f"  {slug}: SKIP (exists)")
        continue
    print(f"  {slug}...", end=" ")
    download(url, out)
    time.sleep(1)
