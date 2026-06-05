import re

HOTEL_IMAGES = {
    "Four Seasons": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    "Ritz Carlton": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    "Shangri-La": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    "Hilton": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "Marriott": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    "Kempinski": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "InterContinental": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    "Hyatt": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    "Sheraton": "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "Radisson": "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    "Movenpick": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "Sofitel": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
    "JW Marriott": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    "Fairmont": "https://images.unsplash.com/photo-1549638441-b787d2e11f14?w=800&q=80",
    "St Regis": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "W Hotel": "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "Mandarin Oriental": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    "Banyan Tree": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    "Anantara": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "Orient": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
}

GENERIC_HOTEL_IMAGES = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
]

RESORT_IMAGE = "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80"
BEACH_HOTEL = "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80"
BUDGET_HOTEL = "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80"
LUXURY_HOTEL = "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80"


def find_hotel_image(hotel_name):
    for name, url in HOTEL_IMAGES.items():
        if name.lower() in hotel_name.lower():
            return url
    return None


def inject_hotel_images(body):
    lines = body.split("\n")
    result = []
    hotel_count = 0

    for line in lines:
        result.append(line)
        hotel_match = re.search(r"(?:отель|Hotel|Resort|отеля)\s+[\"«]?([A-ZА-Я][A-Za-zА-Яа-я\s\-']+?)[\"»]?", line, re.IGNORECASE)
        if hotel_match:
            hotel_name = hotel_match.group(1).strip()
            img_url = find_hotel_image(hotel_name)
            if not img_url:
                if "люкс" in line.lower() or "luxury" in line.lower() or "5 звезд" in line.lower() or "5 star" in line.lower():
                    img_url = LUXURY_HOTEL
                elif "бюджет" in line.lower() or "budget" in line.lower() or "хостел" in line.lower() or "hostel" in line.lower():
                    img_url = BUDGET_HOTEL
                elif "пляж" in line.lower() or "beach" in line.lower() or "курорт" in line.lower() or "resort" in line.lower():
                    img_url = RESORT_IMAGE
                else:
                    img_url = GENERIC_HOTEL_IMAGES[hotel_count % len(GENERIC_HOTEL_IMAGES)]
                    hotel_count += 1
            if img_url and "https://" not in line:
                result.append(f'<img src="{img_url}" alt="{hotel_name}" loading="lazy" style="width:100%;max-height:400px;object-fit:cover;margin:12px 0;">')

    return "\n".join(result)


def inject_attraction_images(body):
    markers = [
        (r"(достопримечательност\w+|attraction\w+|must.?see|must.?visit)", "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&q=80"),
        (r"(храм|temple|мечеть|mosque|церковь|church)", "https://images.unsplash.com/photo-1548013146-72479767bada?w=800&q=80"),
        (r"(пляж|beach|побережье|coastline)", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80"),
        (r"(рынок|market|bazaar|bazar)", "https://images.unsplash.com/photo-1555529771-835f59fc5efe?w=800&q=80"),
        (r"(музей|museum)", "https://images.unsplash.com/photo-1565254973041-83c5f334d19e?w=800&q=80"),
        (r"(гора|mountain|вулкан|volcano)", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"),
    ]
    lines = body.split("\n")
    result = []
    img_inserted = 0

    for i, line in enumerate(lines):
        result.append(line)
        if img_inserted < 4 and "<h2>" in line:
            for pattern, img_url in markers:
                if re.search(pattern, line, re.IGNORECASE):
                    result.append(f'<img src="{img_url}" alt="Attraction" loading="lazy" style="width:100%;max-height:400px;object-fit:cover;margin:16px 0;">')
                    img_inserted += 1
                    break

    return "\n".join(result)
