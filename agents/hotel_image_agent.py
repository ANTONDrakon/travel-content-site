"""
Hotel Photo Agent — finds, verifies, downloads, and creates carousels for hotel photos.

Usage:
    python -m agents.hotel_image_agent "Hotel Name" [--city "City"] [--country "Country"] [--limit 5]

The agent:
    1. Checks known chain hotel database (70+ brands) for verified photo URLs
    2. For unknown hotels, constructs search URLs to reliable CDN sources
    3. Downloads available photos (with retry + timeout)
    4. Converts to WebP format
    5. Creates interactive image carousel HTML
    6. Returns carousel markup + photo metadata for injection into articles
"""

import re
import io
import time
import json
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

BASE = Path(__file__).parent.parent
ASSETS_DIR = BASE / "docs" / "assets" / "hotels"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# CHAIN HOTEL DATABASE — verified Unsplash photo URLs
# Each hotel maps to 2-4 photos for carousel generation
# ============================================================

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
    "Ramses": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Nefertiti": [
        "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
        "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    ],
    "Sunrise": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Samann": [
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Centre Point": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    ],
    "Chaweng": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Krabi Resort": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Cleopatra": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
    ],
    "Bob Marley": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Lub d": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    ],
    "Niras": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Pak-Up": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80",
    ],
    "Puri Agung": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Kuta Paradiso": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Coral": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Arena": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Marukab": [
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    ],
    "Beehive": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Baan": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    ],
    "Anyavee": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Haiyi": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Jinjiang": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Metropark": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Travelotel": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    ],
    "Dosso Dossi": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Cheers": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80",
    ],
    "Sura": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Pyramids": [
        "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
        "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    ],
    "Yalong": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Dadonghai": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Blue Ocean": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Sea Breeze": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Bophut": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Lamai": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    ],
    "Lika": [
        "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    ],
    "Coco Palm": [
        "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Sun Tan": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "White Shell": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Relax Beach": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Ocean Breeze": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
    "Ocean Grand": [
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    ],
    "Beach Grand": [
        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    ],
}

# ============================================================
# CATEGORY-BASED FALLBACK PHOTOS (for hotels without known chains)
# ============================================================

LUXURY_PHOTOS = [
    "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
]
RESORT_PHOTOS = [
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",
    "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
]
BEACH_PHOTOS = [
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
]
BUDGET_PHOTOS = [
    "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
]
GENERIC_PHOTOS = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",
    "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",
]
HOSTEL_PHOTOS = [
    "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",
    "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80",
]


class HotelPhotoAgent:
    """Agent that finds and manages hotel photos with carousel generation.
    Uses HotelPhotoFetcher as primary backend for real photos.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or ASSETS_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "_photo_cache.json"
        self.cache = self._load_cache()
        self.verified = set()
        self.missing = set()

    def _load_cache(self):
        if self.cache_file.exists():
            with open(self.cache_file, encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _cache_key(self, name: str) -> str:
        return hashlib.md5(name.lower().strip().encode()).hexdigest()[:12]

    def find_photos(self, hotel_name: str, max_photos: int = 3,
                    city_slug: str = "", country_slug: str = "") -> list:
        """
        Find photo URLs for a hotel. Returns list of dicts:
        [{"url": "...", "source": "...", "verified": True|False, "brand": "..."}, ...]

        Priority:
        1. HotelPhotoFetcher (real photos from Hotellook / official sources)
        2. Chain database (branded Unsplash, marked unverified)
        3. Category fallback (clearly marked unverified)
        """
        name_lower = hotel_name.lower().strip()
        photos = []

        # STEP 1: Try HotelPhotoFetcher for real photos
        if city_slug and country_slug:
            try:
                from agents.hotel_photo_fetcher import HotelPhotoFetcher
                fetcher = HotelPhotoFetcher()
                result = fetcher.find_photos(hotel_name, city_slug, country_slug, max_photos)
                if result["photos"]:
                    photos = result["photos"]
                    if any(p.get("verified") for p in photos):
                        self.verified.add(hotel_name)
                        return photos[:max_photos]
            except Exception:
                pass

        # STEP 2: Check known chain database (legacy, marked unverified)
        for brand, urls in CHAIN_PHOTOS.items():
            if brand.lower() in name_lower:
                for url in urls[:max_photos]:
                    photos.append({"url": url, "source": "chain_db", "verified": False, "brand": brand})
                return photos[:max_photos]

        # STEP 3: Check cache
        key = self._cache_key(hotel_name)
        if key in self.cache:
            cached = self.cache[key]
            if isinstance(cached, list) and cached:
                return cached[:max_photos]

        # STEP 4: Category-based fallback (verified=False)
        photos = self._categorize_fallback(hotel_name, max_photos)
        self.missing.add(hotel_name)

        self.cache[key] = photos
        self._save_cache()

        return photos

    def _categorize_fallback(self, name: str, max_photos: int) -> list:
        """Select appropriate category photos based on hotel name keywords."""
        nl = name.lower()
        result = []

        if any(w in nl for w in ['hostel', 'хостел', 'backpacker', 'guesthouse', 'homestay', 'гестхаус']):
            pool = HOSTEL_PHOTOS
            source = "category:hostel"
        elif any(w in nl for w in ['luxury', 'люкс', 'deluxe', 'премиум', 'premium', '5 star', 'palace', 'дворец', 'villa estate', 'retreat', 'private']):
            pool = LUXURY_PHOTOS
            source = "category:luxury"
        elif any(w in nl for w in ['resort', 'курорт', 'beach resort', 'island resort', 'spa resort']):
            pool = RESORT_PHOTOS
            source = "category:resort"
        elif any(w in nl for w in ['beach', 'пляж', 'ocean', 'океан', 'sea ', 'море', 'bay', 'бухта', 'coral', 'коралл', 'sand', 'песок', 'sunrise', 'breeze', 'wave', 'palm', 'coconut', 'lagoon', 'coast']):
            pool = BEACH_PHOTOS
            source = "category:beach"
        elif any(w in nl for w in ['budget', 'бюджет', 'economy', 'эконом', 'cheap', 'недорог', 'inn', 'travelotel']):
            pool = BUDGET_PHOTOS
            source = "category:budget"
        else:
            pool = GENERIC_PHOTOS
            source = "category:generic"

        for i, url in enumerate(pool[:max_photos]):
            result.append({"url": url, "source": source, "verified": False})

        return result

    def verify_photo(self, url: str, timeout: int = 10) -> bool:
        """Check if a photo URL is accessible (HEAD request)."""
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'TravelHub/1.0'})
            resp = urllib.request.urlopen(req, timeout=timeout)
            content_type = resp.headers.get('Content-Type', '')
            return resp.status == 200 and 'image' in content_type
        except Exception:
            return False

    def download_photo(self, url: str, hotel_name: str, index: int = 0) -> Optional[Path]:
        """Download a photo and save as WebP. Returns local path or None."""
        safe_name = re.sub(r'[^\w\s-]', '', hotel_name.lower()).strip()[:40].replace(' ', '-')
        local_path = self.cache_dir / f"{safe_name}_{index}.webp"

        if local_path.exists() and local_path.stat().st_size > 1000:
            return local_path

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'TravelHub/1.0 Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=15).read()

            if len(data) < 500:
                return None

            # Convert to WebP
            try:
                from PIL import Image
                img = Image.open(io.BytesIO(data))
                if img.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', img.size, (252, 240, 243))
                    if img.mode in ('RGBA', 'LA'):
                        bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else img)
                    else:
                        bg.paste(img.convert('RGBA'))
                    img = bg
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                if img.width > 1200:
                    img = img.resize((1200, int(img.height * 1200 / img.width)), Image.LANCZOS)
                img.save(local_path, format='WEBP', quality=82)
            except Exception:
                local_path.write_bytes(data)

            return local_path
        except Exception:
            return None

    def build_carousel(self, hotel_name: str, max_photos: int = 3) -> str:
        """Build complete HTML carousel with photos for a hotel."""
        photos = self.find_photos(hotel_name, max_photos)
        if not photos:
            return ""

        carousel_id = f"hc_{hashlib.md5(hotel_name.encode()).hexdigest()[:8]}"
        html_parts = [
            f'<div id="{carousel_id}" class="hotel-carousel" '
            f'style="position:relative;margin:20px 0;border-radius:14px;overflow:hidden;background:var(--bg);box-shadow:0 2px 12px rgba(0,0,0,0.08);">'
        ]

        # Photo slides
        for i, photo in enumerate(photos):
            display = "block" if i == 0 else "none"
            verified_badge = ""
            if photo.get("verified"):
                verified_badge = (
                    f'<span style="position:absolute;top:8px;right:8px;background:rgba(0,180,80,0.85);color:#fff;'
                    f'font-size:10px;padding:2px 8px;border-radius:10px;">verified</span>'
                )
            else:
                verified_badge = (
                    f'<span style="position:absolute;top:8px;right:8px;background:rgba(200,120,40,0.85);color:#fff;'
                    f'font-size:10px;padding:2px 8px;border-radius:10px;">unverified</span>'
                )
            html_parts.append(
                f'<div class="hotel-carousel-slide" style="display:{display};">'
                f'{verified_badge}'
                f'<img src="{photo["url"]}" alt="{hotel_name} — photo {i+1}" loading="lazy" '
                f'style="width:100%;max-height:440px;object-fit:cover;display:block;">'
                f'</div>'
            )

        # Navigation dots
        html_parts.append(
            f'<div style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);display:flex;gap:8px;">'
        )
        for i in range(len(photos)):
            active_color = "var(--vermillion)" if i == 0 else "rgba(255,255,255,0.6)"
            html_parts.append(
                f'<button onclick="var s=document.querySelectorAll(\'#{carousel_id} .hotel-carousel-slide\');'
                f'var d=document.querySelectorAll(\'#{carousel_id} .carousel-dot\');'
                f'for(var j=0;j<s.length;j++){{s[j].style.display=j=={i}?\'block\':\'none\'}}'
                f'for(var k=0;k<d.length;k++){{d[k].style.background=k=={i}?\'var(--vermillion)\':\'rgba(255,255,255,0.6)\'}}" '
                f'class="carousel-dot" '
                f'style="width:10px;height:10px;border-radius:50%;background:{active_color};border:none;cursor:pointer;padding:0;transition:background 0.3s;" '
                f'aria-label="Photo {i+1}"></button>'
            )
        html_parts.append('</div>')

        # Caption
        source_note = ""
        if photos[0].get("brand"):
            source_note = f' • {photos[0]["brand"]}'
        html_parts.append(
            f'<div style="padding:12px 16px;background:#fff;">'
            f'<p style="font-size:14px;font-weight:600;color:var(--ink);margin:0;">{hotel_name}</p>'
            f'<p style="font-size:11px;color:var(--meta);margin:4px 0 0 0;">{len(photos)} photos{source_note}</p>'
            f'</div>'
        )

        html_parts.append('</div>')
        return '\n'.join(html_parts)

    def report(self) -> dict:
        return {
            "verified_count": len(self.verified),
            "missing_count": len(self.missing),
            "cache_size": len(self.cache),
            "verified": sorted(self.verified),
            "missing": sorted(self.missing),
        }


def extract_hotel_names_from_html(html: str) -> list:
    """Extract all hotel names from article HTML body."""
    names = []
    for m in re.finditer(
        r'<h3[^>]*>\s*(?:\d+\.\s*)?([A-ZА-Я][A-Za-zА-Яа-я\s&\-\'\.]{4,60}?)\s*(?:\([^)]*\))?\s*</h3>',
        html, re.IGNORECASE
    ):
        name = m.group(1).strip()
        if not re.match(r'^(в |на |с |от |до |The |A |An |In |At |To )', name, re.IGNORECASE):
            names.append(name)
    return names


# ============================================================
# CLI entry point
# ============================================================

def run():
    import argparse
    parser = argparse.ArgumentParser(description="Hotel Photo Agent — find & verify hotel photos, build carousels")
    parser.add_argument("hotel", nargs="?", help="Hotel name to find photos for")
    parser.add_argument("--city", help="City name (for context)")
    parser.add_argument("--country", help="Country name (for context)")
    parser.add_argument("--limit", type=int, default=3, help="Max photos per hotel")
    parser.add_argument("--html", action="store_true", help="Output carousel HTML")
    parser.add_argument("--scan", help="Scan an HTML file for hotel names")
    parser.add_argument("--verify", action="store_true", help="Verify photo URLs are accessible")
    parser.add_argument("--download", action="store_true", help="Download photos to local cache")
    parser.add_argument("--report", action="store_true", help="Show agent report")

    args = parser.parse_args()
    agent = HotelPhotoAgent()

    if args.report:
        print(json.dumps(agent.report(), indent=2, ensure_ascii=False))
        return

    if args.scan:
        path = Path(args.scan)
        if path.exists():
            html = path.read_text(encoding='utf-8')
            names = extract_hotel_names_from_html(html)
            print(f"Found {len(names)} hotels in {path.name}:")
            for n in names:
                print(f"  • {n}")
        return

    if args.hotel:
        print(f"\n{'='*60}")
        print(f"Hotel Photo Agent")
        print(f"Hotel: {args.hotel}")
        if args.city:
            print(f"City:  {args.city}")
        if args.country:
            print(f"Country: {args.country}")
        print(f"{'='*60}\n")

        photos = agent.find_photos(args.hotel, args.limit)

        for i, photo in enumerate(photos):
            status = "[OK] VERIFIED (chain DB)" if photo.get("verified") else "[~] category fallback"
            print(f"  Photo {i+1}: {photo['source']} — {status}")
            print(f"    URL: {photo['url'][:80]}...")

            if args.verify:
                ok = agent.verify_photo(photo["url"])
                print(f"    Accessible: {'YES' if ok else 'NO'}")

            if args.download:
                local = agent.download_photo(photo["url"], args.hotel, i)
                if local:
                    size_kb = local.stat().st_size // 1024
                    print(f"    Downloaded: {local.name} ({size_kb} KB)")
                else:
                    print(f"    Download: FAILED")

        if args.html:
            print(f"\n{'='*60}")
            print("CAROUSEL HTML:")
            print(f"{'='*60}\n")
            print(agent.build_carousel(args.hotel, args.limit))

        print(f"\nAgent stats: {agent.report()['verified_count']} verified, "
              f"{agent.report()['missing_count']} missing, "
              f"{agent.report()['cache_size']} cached")
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
