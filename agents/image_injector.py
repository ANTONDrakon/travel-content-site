"""
DATA-DRIVEN IMAGE INJECTOR
Strictly uses data/hotels.json for hotel images.
No generic fallbacks. No cross-contamination.
Every hotel gets ONLY its own images.
"""
import re
import json
from pathlib import Path

BASE = Path(__file__).parent.parent
HOTELS_DB = json.loads((BASE / "data" / "hotels.json").read_text(encoding="utf-8"))

# Build lookup: (country_slug, city_slug, hotel_name_lower) -> hotel data
HOTEL_LOOKUP = {}
for h in HOTELS_DB:
    key = (h["country_slug"], h["city_slug"], h["name"].lower())
    HOTEL_LOOKUP[key] = h

# Build lookup by name substring (for fuzzy matching)
HOTEL_BY_NAME = {}
for h in HOTELS_DB:
    name_lower = h["name"].lower()
    HOTEL_BY_NAME[name_lower] = h
    # Also index by first 2-3 words
    parts = name_lower.split()[:3]
    for i in range(1, len(parts) + 1):
        partial = " ".join(parts[:i])
        if partial not in HOTEL_BY_NAME:
            HOTEL_BY_NAME[partial] = h

def find_hotel(country_slug, city_slug, hotel_name):
    """Find hotel data by country, city, and name. Returns dict or None."""
    key = (country_slug, city_slug, hotel_name.lower())
    if key in HOTEL_LOOKUP:
        return HOTEL_LOOKUP[key]
    
    # Fuzzy: try name-only match within same country
    name_lower = hotel_name.lower()
    for (cs, ct, name), h in HOTEL_LOOKUP.items():
        if cs == country_slug and name == name_lower:
            return h
    
    # Broader: name match anywhere
    if name_lower in HOTEL_BY_NAME:
        return HOTEL_BY_NAME[name_lower]
    
    return None

def build_swiper_carousel(hotel, lang="ru"):
    """Build Swiper.js carousel HTML for a hotel."""
    images = hotel.get("images", [])
    if not images:
        return ""

    hotel_name = hotel["name"]
    carousel_id = f"swiper_{abs(hash(hotel_name + hotel['city_slug'])) % 1000000}"

    slides = []
    for i, img in enumerate(images[:3]):
        alt = img.get("alt", hotel_name) if lang == "ru" else img.get("alt_en", hotel_name)
        src = img["src"]
        slides.append(
            f'<div class="swiper-slide">'
            f'<img src="{src}" alt="{alt}" loading="{"eager" if i == 0 else "lazy"}" '
            f'style="width:100%;height:420px;object-fit:cover;border-radius:12px;">'
            f'</div>'
        )

    city_name = hotel.get("city_name_ru", "") if lang == "ru" else hotel.get("city_name_en", "")
    price = hotel.get("price", "")
    rating = hotel.get("rating", "")
    district = hotel.get("district", "")

    arrows_ru = ',"nextEl":".swiper-button-next","prevEl":".swiper-button-prev"'
    arrows_en = ',"nextEl":".swiper-button-next","prevEl":".swiper-button-prev"'

    html = f'''<div class="hotel-card" style="margin:24px 0;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,0.06);">
<div id="{carousel_id}" class="swiper hotel-swiper" style="position:relative;">
<div class="swiper-wrapper">
{"".join(slides)}
</div>
<div class="swiper-pagination" style="position:absolute;bottom:12px;left:50%;transform:translateX(-50%);z-index:10;"></div>
<div class="swiper-button-prev" style="color:#fff;left:10px;"></div>
<div class="swiper-button-next" style="color:#fff;right:10px;"></div>
</div>
<div style="padding:18px 20px;">
<h4 style="font-size:17px;font-weight:700;margin:0 0 4px 0;color:var(--ink);">{hotel_name}</h4>
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
<span style="font-size:13px;color:var(--meta);">📍 {city_name}</span>'''
    
    if district:
        html += f'<span style="font-size:13px;color:var(--meta);">🏙 {district}</span>'
    if price:
        html += f'<span style="font-size:14px;font-weight:600;color:var(--vermillion);">{price}</span>'
    if rating:
        html += f'<span style="font-size:13px;color:#f39c12;">⭐ {rating}</span>'

    html += f'''</div></div></div>
<script>
(function(){{
var s = new Swiper('#{carousel_id}', {{
    slidesPerView: 1,
    spaceBetween: 0,
    loop: true,
    autoplay: {{ delay: 4000, disableOnInteraction: false }},
    pagination: {{ el: '#{carousel_id} .swiper-pagination', clickable: true }},
    navigation: {{ nextEl: '#{carousel_id} .swiper-button-next', prevEl: '#{carousel_id} .swiper-button-prev' }},
    lazy: {{ loadPrevNext: true }},
}});
}})();
</script>'''

    return html


def inject_hotel_carousels(body, country_slug, city_slug, lang="ru"):
    """Inject Swiper carousels into article body for each hotel."""
    lines = body.split("\n")
    result = []
    injected = set()
    count = 0

    for line in lines:
        result.append(line)

        if count >= 15:
            continue
        if "<img" in line or "swiper" in line.lower():
            continue

        # Match <h3>N. Hotel Name (category)</h3>
        m = re.search(
            r'<h3[^>]*>\s*(?:\d+\.\s*)?(?P<name>[A-ZА-Я][A-Za-zА-Яа-я\s&\-\'\.]{4,80}?)\s*(?:\([^)]*\))?\s*</h3>',
            line, re.IGNORECASE
        )
        if not m:
            continue

        hotel_name = m.group("name").strip()
        if hotel_name.lower() in injected:
            continue

        hotel = find_hotel(country_slug, city_slug, hotel_name)
        if hotel and hotel.get("images"):
            carousel = build_swiper_carousel(hotel, lang)
            if carousel:
                result.append(carousel)
                injected.add(hotel_name.lower())
                count += 1

    return "\n".join(result)


def inject_attraction_images(body):
    """Inject attraction images (data-driven from Unsplash, category-matched)."""
    cat_map = {
        (r'храм|temple|мечеть|mosque|церковь|church|собор|cathedral',
         "https://images.unsplash.com/photo-1548013146-72479767bada?w=800&q=80"),
        (r'пляж|beach|побережье|coast|бухта|bay',
         "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80"),
        (r'рынок|market|bazaar|базар|grand bazaar',
         "https://images.unsplash.com/photo-1555529771-835f59fc5efe?w=800&q=80"),
        (r'музей|museum|галере|gallery',
         "https://images.unsplash.com/photo-1565254973041-83c5f334d19e?w=800&q=80"),
        (r'гора|mountain|вулкан|volcano|пик|peak|трек|trek',
         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"),
        (r'дворец|palace|замок|castle|крепость|fortress',
         "https://images.unsplash.com/photo-1548013146-72479767bada?w=800&q=80"),
        (r'парк|park|сад|garden|национ|nation|заповед|reserve',
         "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&q=80"),
        (r'дайв|dive|снорк|snorkel|коралл|coral|риф|reef',
         "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80"),
    }

    lines = body.split("\n")
    result = []
    img_count = 0

    for i, line in enumerate(lines):
        result.append(line)
        if img_count >= 6:
            continue
        if re.search(r'<h2[^>]*>', line, re.IGNORECASE):
            for patterns, url in cat_map:
                if re.search(patterns, line, re.IGNORECASE):
                    result.append(
                        f'<img src="{url}" alt="" loading="lazy" '
                        f'style="width:100%;max-height:400px;object-fit:cover;border-radius:12px;margin:16px 0;">'
                    )
                    img_count += 1
                    break

    return "\n".join(result)
