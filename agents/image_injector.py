"""Inject real hotel/attraction images with carousels into article bodies."""
import re
from agents.hotel_image_agent import HotelPhotoAgent

_hotel_agent = HotelPhotoAgent()

KNOWN_HOTEL_BRANDS = [
    "Four Seasons", "Ritz-Carlton", "Ritz Carlton", "Shangri-La", "Shangri La",
    "Hilton", "Marriott", "JW Marriott", "Kempinski", "InterContinental",
    "Intercontinental", "Hyatt", "Sheraton", "Radisson", "Movenpick",
    "Sofitel", "Fairmont", "St Regis", "St. Regis", "W Hotel", "W Hotels",
    "Mandarin Oriental", "Banyan Tree", "Anantara", "Peninsula", "Orient",
    "Conrad", "Waldorf", "Rosewood", "Six Senses", "Aman", "Como",
    "Park Hyatt", "Grand Hyatt", "Renaissance", "Le Meridien",
    "Swissotel", "Raffles", "Novotel", "Holiday Inn", "Pullman",
    "Steigenberger", "Rixos", "Jaz", "Oberoi", "Mulia", "One&Only",
    "Cinnamon", "OZEN", "Pickalbatros", "Capella", "Amari", "RedDoorz",
    "Grand Inna", "Amnaya", "Padma", "Amaris", "Solymar", "Hotel Jen",
    "Kaani", "Grandmas", "Wanda", "Zizhu", "Centre Point", "Lub d",
    "Niras", "Samann", "Chaweng Regent", "Krabi Resort", "Ramses",
    "Nefertiti", "Sunrise", "Cleopatra", "Bob Marley", "Pak-Up",
    "Puri Agung", "Kuta Paradiso", "Coral", "Arena", "Marukab",
    "Beehive", "Baan", "Anyavee", "Haiyi", "Jinjiang", "Metropark",
    "Travelotel", "Dosso Dossi", "Cheers", "Sura", "Pyramids",
    "Yalong", "Dadonghai", "Blue Ocean", "Sea Breeze", "Bophut",
    "Lamai", "Lika", "Coco Palm", "Sun Tan", "White Shell",
    "Relax Beach", "Ocean Breeze", "Ocean Grand", "Beach Grand",
]

def build_carousel_html(photos, hotel_name):
    """Build image carousel from photo dicts."""
    if not photos:
        return ""
    photos = photos[:3]
    if len(photos) == 1:
        return (
            f'<div style="margin:16px 0;">'
            f'<img src="{photos[0]["url"]}" alt="{hotel_name}" loading="lazy" '
            f'style="width:100%;max-height:420px;object-fit:cover;border-radius:12px;">'
            f'<p style="font-size:12px;color:var(--meta);margin-top:6px;text-align:center;">{hotel_name}</p></div>'
        )
    carousel_id = f"hc_{abs(hash(hotel_name)) % 1000000}"
    html = [f'<div id="{carousel_id}" class="hotel-carousel" style="position:relative;margin:16px 0;border-radius:12px;overflow:hidden;background:var(--bg);">']
    for i, p in enumerate(photos):
        d = "block" if i == 0 else "none"
        html.append(f'<div class="hc-slide" style="display:{d};"><img src="{p["url"]}" alt="{hotel_name} - {i+1}" loading="lazy" style="width:100%;max-height:420px;object-fit:cover;display:block;"></div>')
    html.append(f'<div style="position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px;">')
    for i in range(len(photos)):
        bg = "var(--vermillion)" if i == 0 else "rgba(255,255,255,0.6)"
        html.append(f'<button onclick="var s=document.querySelectorAll(\'#{carousel_id} .hc-slide\');var d=document.querySelectorAll(\'#{carousel_id} .hc-dot\');for(var j=0;j<s.length;j++){{s[j].style.display=j=={i}?\'block\':\'none\';d[j].style.background=j=={i}?\'var(--vermillion)\':\'rgba(255,255,255,0.6)\'}}" class="hc-dot" style="width:8px;height:8px;border-radius:50%;background:{bg};border:none;cursor:pointer;padding:0;" aria-label="Photo {i+1}"></button>')
    html.append(f'</div><p style="font-size:12px;color:var(--meta);margin:8px 0 0 12px;">{hotel_name} &bull; {len(photos)} photos</p></div>')
    return '\n'.join(html)


def inject_hotel_images(body):
    """Inject hotel images into article body with real photos and carousels."""
    lines = body.split("\n")
    result = []
    hotel_count = 0
    used_brands = set()

    for line in lines:
        result.append(line)

        if hotel_count >= 10:
            continue

        if "<img" in line or "carousel" in line:
            continue

        hotel_name = None

        # Pattern 1: <h3> N. Hotel Name (category) </h3>
        m = re.search(r'<h3[^>]*>\s*(?:\d+\.\s*)?([A-ZА-Я][A-Za-zА-Яа-я\s&\-\'\.]{4,60}?)\s*(?:\([^)]*\))?\s*</h3>', line, re.IGNORECASE)
        if m:
            hotel_name = m.group(1).strip()

        # Pattern 2: Known hotel brands
        if not hotel_name:
            for brand in KNOWN_HOTEL_BRANDS:
                if brand.lower() in line.lower() and brand.lower() not in used_brands:
                    # Find the broader context of the name
                    idx = line.lower().find(brand.lower())
                    end_idx = idx + len(brand)
                    # Extend to include rest of hotel name (e.g., "Hilton Sanya Resort & Spa")
                    while end_idx < len(line) and line[end_idx] not in '<([':
                        end_idx += 1
                    hotel_name = line[idx:end_idx].strip()
                    used_brands.add(brand.lower())
                    break

        if hotel_name and len(hotel_name) >= 3:
            photos = _hotel_agent.find_photos(hotel_name, max_photos=3)
            if photos:
                carousel = build_carousel_html(photos, hotel_name)
                result.append(carousel)
                hotel_count += 1

    return "\n".join(result)


def inject_attraction_images(body):
    """Inject attraction images based on H2 heading categories."""
    category_map = {
        (r'храм|temple|мечеть|mosque|церковь|church|собор|cathedral|монастырь|monastery',
         "https://images.unsplash.com/photo-1548013146-72479767bada?w=800&q=80"),
        (r'пляж|beach|побережье|coast|бухта|bay|лагун|lago',
         "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80"),
        (r'рынок|market|bazaar|базар|торгов|shop|mall|grand bazaar',
         "https://images.unsplash.com/photo-1555529771-835f59fc5efe?w=800&q=80"),
        (r'музей|museum|галере|gallery|выстав|exhibit',
         "https://images.unsplash.com/photo-1565254973041-83c5f334d19e?w=800&q=80"),
        (r'гора|mountain|вулкан|volcano|пик|peak|восхож|trek|hiking',
         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"),
        (r'дворец|palace|замок|castle|крепость|fortress',
         "https://images.unsplash.com/photo-1548013146-72479767bada?w=800&q=80"),
        (r'парк|park|сад|garden|национ|nation|заповед|reserve',
         "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&q=80"),
        (r'дайв|dive|снорк|snorkel|коралл|coral|риф|reef',
         "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80"),
        (r'ресторан|restaurant|кафе|cafe|еда|food|кухня|cuisine|гастро|gastro',
         "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80"),
        (r'спа|spa|массаж|massage|йога|yoga|оздоров|wellness',
         "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800&q=80"),
    }

    lines = body.split("\n")
    result = []
    img_inserted = 0
    last_h2_pos = -1

    for i, line in enumerate(lines):
        result.append(line)

        if img_inserted >= 6:
            continue

        if re.search(r'<h2[^>]*>', line, re.IGNORECASE) and i > last_h2_pos:
            for patterns, img_url in category_map:
                if re.search(patterns, line, re.IGNORECASE):
                    result.append(
                        f'<img src="{img_url}" alt="" loading="lazy" '
                        f'style="width:100%;max-height:400px;object-fit:cover;border-radius:12px;margin:16px 0;">'
                    )
                    img_inserted += 1
                    last_h2_pos = i
                    break

    return "\n".join(result)
