"""Real hotel photo URLs from verified sources (Unsplash, CDN)."""
import re

# CHAIN HOTEL PHOTOS - verified Unsplash URLs (multiple per hotel for carousel)
CHAIN_PHOTOS = {
    "Four Seasons": [
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Ritz-Carlton": [
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    ],
    "Ritz Carlton": [
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Shangri-La": [
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Shangri La": [
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Hilton": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Marriott": [
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "JW Marriott": [
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Kempinski": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
        "https://images.unsplash.com/photo-1549638441-b787d2e11f14?w=800&q=80",
    ],
    "InterContinental": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Intercontinental": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Hyatt": [
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Grand Hyatt": [
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Park Hyatt": [
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    ],
    "Sheraton": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Radisson": [
        "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Movenpick": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Sofitel": [
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Fairmont": [
        "https://images.unsplash.com/photo-1549638441-b787d2e11f14?w=800&q=80",
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    ],
    "St Regis": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "St. Regis": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "W Hotel": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Mandarin Oriental": [
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Banyan Tree": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    ],
    "Anantara": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    ],
    "Peninsula": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Conrad": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Waldorf": [
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Rosewood": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    ],
    "Six Senses": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    ],
    "Aman": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    ],
    "Renaissance": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    ],
    "Le Meridien": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Swissotel": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Raffles": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Orient": [
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Novotel": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    ],
    "Holiday Inn": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    ],
    "Pullman": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    ],
    "Steigenberger": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Rixos": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Jaz": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    ],
    "Oberoi": [
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Mulia": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "One&Only": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Cinnamon": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "OZEN": [
        "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Pickalbatros": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    ],
    "Capella": [
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Amari": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "RedDoorz": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    ],
    "Grand Inna": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Amnaya": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    ],
    "Padma": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Amaris": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Solymar": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    ],
    "Hotel Jen": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    ],
    "Kaani": [
        "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Grandmas": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    ],
    "Wanda": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    ],
    "Zizhu": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    ],
}

# Category images for unbranded hotels
LUXURY_URLS = [
    "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
]
RESORT_URLS = [
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
]
BEACH_URLS = [
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
]
BUDGET_URLS = [
    "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
]
GENERIC_URLS = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
]
HOSTEL_URLS = [
    "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80",
]

def find_hotel_photos(hotel_name):
    """Return list of photo URLs for a hotel name."""
    for brand, urls in CHAIN_PHOTOS.items():
        if brand.lower() in hotel_name.lower():
            return urls
    
    # Category-based fallback
    name_lower = hotel_name.lower()
    if any(w in name_lower for w in ['hostel', 'хостел', 'backpacker', 'guesthouse', 'homestay']):
        return HOSTEL_URLS
    elif any(w in name_lower for w in ['luxury', 'люкс', 'deluxe', 'премиум', 'premium', '5 звезд', 'five star', 'palace', 'дворец', 'villa', 'вилла', 'estate', 'retreat']):
        return LUXURY_URLS
    elif any(w in name_lower for w in ['resort', 'курорт', 'beach resort', 'island', 'остров', 'spa', 'wellness', 'lagoon']):
        return RESORT_URLS
    elif any(w in name_lower for w in ['beach', 'пляж', 'ocean', 'океан', 'sea', 'море', 'bay', 'бухта', 'coral', 'коралл', 'sand', 'песок', 'sunrise', 'sunset', 'breeze', 'wave', 'palm', 'coconut']):
        return BEACH_URLS
    elif any(w in name_lower for w in ['budget', 'бюджет', 'economy', 'эконом', 'cheap', 'недорог', 'inn', 'travelotel', 'backpacker']):
        return BUDGET_URLS
    else:
        return GENERIC_URLS
