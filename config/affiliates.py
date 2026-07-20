import os

MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "736226")

# ---------------------------------------------------------------------------
# SERVICE REGISTRY — single source of truth for all affiliate services
# ---------------------------------------------------------------------------

SERVICE_REGISTRY = {
    # ── Flights ──────────────────────────────────────────────────────────
    "aviasales": {
        "name": "Aviasales",
        "category": "flights",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3770&source_type=link&type=click&campaign_id=100&trs=aviasales",
        "langs": ["ru", "en"],
        "aliases": ["Aviasales", "Авиасейлс"],
    },
    "kiwi": {
        "name": "Kiwi.com",
        "category": "flights",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3799&source_type=link&type=click&campaign_id=114&trs=kiwicom",
        "langs": ["en", "es"],
        "aliases": ["Kiwi.com", "Kiwi"],
    },
    "trip": {
        "name": "Trip.com",
        "category": "flights",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3802&source_type=link&type=click&campaign_id=119&trs=tripcom",
        "langs": ["en", "es"],
        "aliases": ["Trip.com"],
    },
    "skyscanner": {
        "name": "Skyscanner",
        "category": "flights",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3804&source_type=link&type=click&campaign_id=160&trs=skyscanner",
        "langs": ["en", "es"],
        "aliases": ["Skyscanner", "Escáner de vuelos"],
    },
    "edreams": {
        "name": "eDreams",
        "category": "flights",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3805&source_type=link&type=click&campaign_id=161&trs=edreams",
        "langs": ["es", "en"],
        "aliases": ["eDreams", "edreams", "eDreams ODIGEO"],
    },

    # ── Hotels ───────────────────────────────────────────────────────────
    "hotellook": {
        "name": "Hotellook",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3772&source_type=link&type=click&campaign_id=101&trs=hotellook",
        "langs": ["ru", "en"],
        "aliases": ["Hotellook", "Хотеллук"],
    },
    "booking": {
        "name": "Booking.com",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3776&source_type=link&type=click&campaign_id=108&trs=booking",
        "langs": ["en", "es"],
        "aliases": ["Booking.com", "Booking"],
    },
    "agoda": {
        "name": "Agoda",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3779&source_type=link&type=click&campaign_id=110&trs=agoda",
        "langs": ["en", "es"],
        "aliases": ["Agoda"],
    },
    "ostrovok": {
        "name": "Ostrovok",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4128&source_type=link&type=click&campaign_id=122&trs=ostrovok",
        "langs": ["ru"],
        "aliases": ["Ostrovok", "Островок"],
    },
    "sutochno": {
        "name": "Суточно.ру",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4129&source_type=link&type=click&campaign_id=123&trs=sutochno",
        "langs": ["ru"],
        "aliases": ["Суточно.ру", "Sutochno", "sutochno.ru"],
    },
    "edreams_hotels": {
        "name": "eDreams Hoteles",
        "category": "hotels",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3806&source_type=link&type=click&campaign_id=162&trs=edreams_hotels",
        "langs": ["es"],
        "aliases": ["eDreams Hoteles", "eDreams Hotels"],
    },

    # ── Tours ────────────────────────────────────────────────────────────
    "level": {
        "name": "Level.Travel",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3774&source_type=link&type=click&campaign_id=103&trs=level",
        "langs": ["ru", "en"],
        "aliases": ["Level.Travel", "Level", "Level Travel"],
    },
    "travelata": {
        "name": "Travelata",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4130&source_type=link&type=click&campaign_id=124&trs=travelata",
        "langs": ["ru"],
        "aliases": ["Travelata", "Травелата"],
    },
    "sletat": {
        "name": "Слетать.РФ",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4131&source_type=link&type=click&campaign_id=125&trs=sletat",
        "langs": ["ru"],
        "aliases": ["Слетать.РФ", "Sletat", "sletat.ru"],
    },
    "onlinetours": {
        "name": "OnlineTours",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4132&source_type=link&type=click&campaign_id=126&trs=onlinetours",
        "langs": ["ru"],
        "aliases": ["OnlineTours", "ОнлайнТурсы"],
    },
    "bolshayastrana": {
        "name": "Большая Страна",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4133&source_type=link&type=click&campaign_id=127&trs=bolshayastrana",
        "langs": ["ru"],
        "aliases": ["Большая Страна", "BolshayaStrana"],
    },
    "putevka": {
        "name": "Путёвка",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4134&source_type=link&type=click&campaign_id=128&trs=putevka",
        "langs": ["ru"],
        "aliases": ["Путёвка", "Putevka", "putevka.ru"],
    },
    "ektatraveling": {
        "name": "Экта Трэвел",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4135&source_type=link&type=click&campaign_id=129&trs=ektatraveling",
        "langs": ["ru"],
        "aliases": ["Экта Трэвел", "EktaTraveling"],
    },
    "lavoyage": {
        "name": "LaVoyage",
        "category": "tours",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4136&source_type=link&type=click&campaign_id=130&trs=lavoyage",
        "langs": ["ru", "en"],
        "aliases": ["LaVoyage"],
    },

    # ── Excursions ───────────────────────────────────────────────────────
    "wegotrip": {
        "name": "WeGoTrip",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4137&source_type=link&type=click&campaign_id=131&trs=wegotrip",
        "langs": ["ru", "en"],
        "aliases": ["WeGoTrip"],
    },
    "tripster": {
        "name": "Tripster",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4138&source_type=link&type=click&campaign_id=132&trs=tripster",
        "langs": ["ru", "en"],
        "aliases": ["Tripster"],
    },
    "getyourguide": {
        "name": "GetYourGuide",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3798&source_type=link&type=click&campaign_id=115&trs=getyourguide",
        "langs": ["en", "es"],
        "aliases": ["GetYourGuide"],
    },
    "viator": {
        "name": "Viator",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3775&source_type=link&type=click&campaign_id=107&trs=viator",
        "langs": ["en", "es"],
        "aliases": ["Viator"],
    },
    "klook": {
        "name": "Klook",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3797&source_type=link&type=click&campaign_id=120&trs=klook",
        "langs": ["en", "es"],
        "aliases": ["Klook"],
    },
    "civitatis": {
        "name": "Civitatis",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3807&source_type=link&type=click&campaign_id=163&trs=civitatis",
        "langs": ["es", "en"],
        "aliases": ["Civitatis", "civitatis.com"],
    },
    "hoppa": {
        "name": "Hoppa",
        "category": "excursions",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3808&source_type=link&type=click&campaign_id=164&trs=hoppa",
        "langs": ["en", "es"],
        "aliases": ["Hoppa", "hoppa.com"],
    },

    # ── Transfers ────────────────────────────────────────────────────────
    "kiwitaxi": {
        "name": "Kiwitaxi",
        "category": "transfers",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3782&source_type=link&type=click&campaign_id=112&trs=kiwitaxi",
        "langs": ["ru", "en"],
        "aliases": ["Kiwitaxi"],
    },
    "gettransfer": {
        "name": "GetTransfer",
        "category": "transfers",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4139&source_type=link&type=click&campaign_id=133&trs=gettransfer",
        "langs": ["ru", "en"],
        "aliases": ["GetTransfer", "GetTransfer.com"],
    },
    "intui": {
        "name": "Intui",
        "category": "transfers",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4140&source_type=link&type=click&campaign_id=134&trs=intui",
        "langs": ["ru", "en"],
        "aliases": ["Intui", "Intui.travel"],
    },

    # ── Insurance ────────────────────────────────────────────────────────
    "cherehapa": {
        "name": "Черехапа",
        "category": "insurance",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3773&source_type=link&type=click&campaign_id=102&trs=cherehapa",
        "langs": ["ru"],
        "aliases": ["Черехапа", "Cherehapa", "cherehapa.ru"],
    },
    "sravni": {
        "name": "Сравни.ру",
        "category": "insurance",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4141&source_type=link&type=click&campaign_id=135&trs=sravni",
        "langs": ["ru"],
        "aliases": ["Сравни.ру", "Sravni", "sravni.ru"],
    },
    "tripinsurance": {
        "name": "Tripinsurance",
        "category": "insurance",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4142&source_type=link&type=click&campaign_id=136&trs=tripinsurance",
        "langs": ["ru", "en"],
        "aliases": ["Tripinsurance"],
    },

    # ── eSIM ─────────────────────────────────────────────────────────────
    "airalo": {
        "name": "Airalo",
        "category": "esim",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3803&source_type=link&type=click&campaign_id=118&trs=airalo",
        "langs": ["en"],
        "aliases": ["Airalo"],
    },
    "yesim": {
        "name": "YesIM",
        "category": "esim",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4143&source_type=link&type=click&campaign_id=137&trs=yesim",
        "langs": ["ru", "en"],
        "aliases": ["YesIM"],
    },
    "drimsim": {
        "name": "DrimSIM",
        "category": "esim",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4144&source_type=link&type=click&campaign_id=138&trs=drimsim",
        "langs": ["ru", "en"],
        "aliases": ["DrimSIM", "DrimSim"],
    },

    # ── Car Rental ───────────────────────────────────────────────────────
    "discovercars": {
        "name": "DiscoverCars",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3780&source_type=link&type=click&campaign_id=111&trs=discovercars",
        "langs": ["en"],
        "aliases": ["DiscoverCars"],
    },
    "localrent": {
        "name": "Localrent",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3783&source_type=link&type=click&campaign_id=113&trs=localrent",
        "langs": ["ru", "en"],
        "aliases": ["Localrent"],
    },
    "getrentacar": {
        "name": "GetRentACar",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4145&source_type=link&type=click&campaign_id=139&trs=getrentacar",
        "langs": ["ru"],
        "aliases": ["GetRentACar"],
    },
    "economybookings": {
        "name": "EconomyBookings",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4146&source_type=link&type=click&campaign_id=140&trs=economybookings",
        "langs": ["en"],
        "aliases": ["EconomyBookings"],
    },
    "qeeq": {
        "name": "QEEQ",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4147&source_type=link&type=click&campaign_id=141&trs=qeeq",
        "langs": ["en"],
        "aliases": ["QEEQ"],
    },
    "autoeurope": {
        "name": "AutoEurope",
        "category": "car_rental",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4148&source_type=link&type=click&campaign_id=142&trs=autoeurope",
        "langs": ["en"],
        "aliases": ["AutoEurope"],
    },

    # ── Bikes & Moto ─────────────────────────────────────────────────────
    "bikesbooking": {
        "name": "BikesBooking",
        "category": "bikes",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4149&source_type=link&type=click&campaign_id=143&trs=bikesbooking",
        "langs": ["ru", "en"],
        "aliases": ["BikesBooking"],
    },

    # ── Tickets ──────────────────────────────────────────────────────────
    "tiqets": {
        "name": "Tiqets",
        "category": "tickets",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3801&source_type=link&type=click&campaign_id=116&trs=tiqets",
        "langs": ["en"],
        "aliases": ["Tiqets"],
    },
    "sputnik8": {
        "name": "Sputnik8",
        "category": "tickets",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4150&source_type=link&type=click&campaign_id=144&trs=sputnik8",
        "langs": ["ru"],
        "aliases": ["Sputnik8", "Спутник8"],
    },
    "ticketnetwork": {
        "name": "TicketNetwork",
        "category": "tickets",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4151&source_type=link&type=click&campaign_id=145&trs=ticketnetwork",
        "langs": ["en"],
        "aliases": ["TicketNetwork"],
    },

    # ── Trains ───────────────────────────────────────────────────────────
    "tutu": {
        "name": "Туту.ру",
        "category": "trains",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4152&source_type=link&type=click&campaign_id=146&trs=tutu",
        "langs": ["ru"],
        "aliases": ["Туту.ру", "Tutu", "tutu.ru"],
    },
    "vipzal": {
        "name": "ВИП-зал",
        "category": "trains",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4153&source_type=link&type=click&campaign_id=147&trs=vipzal",
        "langs": ["ru"],
        "aliases": ["ВИП-зал", "VIP-Zal"],
    },

    # ── Buses ────────────────────────────────────────────────────────────
    "unitiki": {
        "name": "Юникей",
        "category": "buses",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4154&source_type=link&type=click&campaign_id=148&trs=unitiki",
        "langs": ["ru"],
        "aliases": ["Юникей", "Unitiki"],
    },
    "12go": {
        "name": "12Go",
        "category": "buses",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4127&source_type=link&type=click&campaign_id=121&trs=12go",
        "langs": ["ru", "en"],
        "aliases": ["12Go", "12Go.Asia"],
    },

    # ── Cruises ──────────────────────────────────────────────────────────
    "kruizonline": {
        "name": "Круиз Онлайн",
        "category": "cruises",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4155&source_type=link&type=click&campaign_id=149&trs=kruizonline",
        "langs": ["ru"],
        "aliases": ["Круиз Онлайн", "Kruiz-Online"],
    },

    # ── Sanatoriums ──────────────────────────────────────────────────────
    "sanatory": {
        "name": "Санаторий",
        "category": "sanatoriums",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4156&source_type=link&type=click&campaign_id=150&trs=sanatory",
        "langs": ["ru"],
        "aliases": ["Санаторий", "Sanatory"],
    },
    "sanatoriums": {
        "name": "Sanatoriums.com",
        "category": "sanatoriums",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4157&source_type=link&type=click&campaign_id=151&trs=sanatoriums",
        "langs": ["ru", "en"],
        "aliases": ["Sanatoriums.com", "Sanatoriums"],
    },

    # ── Camping ──────────────────────────────────────────────────────────
    "mirturbaz": {
        "name": "МирТурбаз",
        "category": "camping",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4158&source_type=link&type=click&campaign_id=152&trs=mirturbaz",
        "langs": ["ru"],
        "aliases": ["МирТурбаз", "MirTurbaz"],
    },

    # ── Luggage Storage ──────────────────────────────────────────────────
    "radicalstorage": {
        "name": "Radical Storage",
        "category": "luggage",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4159&source_type=link&type=click&campaign_id=153&trs=radicalstorage",
        "langs": ["en"],
        "aliases": ["Radical Storage"],
    },

    # ── Yacht Rental ─────────────────────────────────────────────────────
    "searadar": {
        "name": "Searadar",
        "category": "yacht",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4160&source_type=link&type=click&campaign_id=154&trs=searadar",
        "langs": ["ru", "en"],
        "aliases": ["Searadar"],
    },

    # ── Flight Compensation ──────────────────────────────────────────────
    "airhelp": {
        "name": "AirHelp",
        "category": "compensation",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4161&source_type=link&type=click&campaign_id=155&trs=airhelp",
        "langs": ["en"],
        "aliases": ["AirHelp"],
    },
    "compensair": {
        "name": "Compensair",
        "category": "compensation",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=3800&source_type=link&type=click&campaign_id=117&trs=compensair",
        "langs": ["ru", "en"],
        "aliases": ["Compensair"],
    },

    # ── Travel Portal ────────────────────────────────────────────────────
    "yandextravel": {
        "name": "Яндекс Путешествия",
        "category": "portal",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4162&source_type=link&type=click&campaign_id=156&trs=yandextravel",
        "langs": ["ru"],
        "aliases": ["Яндекс Путешествия", "Yandex Travel"],
    },

    # ── Marketplace ──────────────────────────────────────────────────────
    "avito": {
        "name": "Авито",
        "category": "marketplace",
        "url": f"https://tp.media/click?shmarker={MARKER}&promo_id=4163&source_type=link&type=click&campaign_id=157&trs=avito",
        "langs": ["ru"],
        "aliases": ["Авито", "Avito"],
    },
}

# ---------------------------------------------------------------------------
# CATEGORY METADATA — for AI prompts and content generation
# ---------------------------------------------------------------------------

CATEGORIES = {
    "flights": {
        "name_ru": "Авиабилеты",
        "name_en": "Flights",
        "icon": "✈️",
        "description_ru": "Поиск и бронирование авиабилетов",
        "description_en": "Search and book flights",
    },
    "hotels": {
        "name_ru": "Отели",
        "name_en": "Hotels",
        "icon": "🏨",
        "description_ru": "Бронирование отелей и жилья",
        "description_en": "Book hotels and accommodation",
    },
    "tours": {
        "name_ru": "Туры",
        "name_en": "Tours",
        "icon": "🌴",
        "description_ru": "Подбор туров и путёвок",
        "description_en": "Find tour packages",
    },
    "excursions": {
        "name_ru": "Экскурсии",
        "name_en": "Excursions",
        "icon": "🗺️",
        "description_ru": "Экскурсии иguided tours",
        "description_en": "Guided tours and activities",
    },
    "transfers": {
        "name_ru": "Трансферы",
        "name_en": "Transfers",
        "icon": "🚗",
        "description_ru": "Трансферы из аэропорта и по городу",
        "description_en": "Airport and city transfers",
    },
    "insurance": {
        "name_ru": "Страхование",
        "name_en": "Insurance",
        "icon": "🛡️",
        "description_ru": "Страхование путешественников",
        "description_en": "Travel insurance",
    },
    "esim": {
        "name_ru": "eSIM",
        "name_en": "eSIM",
        "icon": "📱",
        "description_ru": "Мобильная связь за рубежом",
        "description_en": "Mobile connectivity abroad",
    },
    "car_rental": {
        "name_ru": "Аренда авто",
        "name_en": "Car Rental",
        "icon": "🚙",
        "description_ru": "Аренда автомобилей",
        "description_en": "Rent a car",
    },
    "bikes": {
        "name_ru": "Аренда мото/велосипедов",
        "name_en": "Bike & Moto Rental",
        "icon": "🏍️",
        "description_ru": "Аренда мотоциклов и велосипедов",
        "description_en": "Rent bikes and motorcycles",
    },
    "tickets": {
        "name_ru": "Билеты",
        "name_en": "Tickets",
        "icon": "🎟️",
        "description_ru": "Билеты на мероприятия и достопримечательности",
        "description_en": "Tickets for events and attractions",
    },
    "trains": {
        "name_ru": "ЖД билеты",
        "name_en": "Train Tickets",
        "icon": "🚂",
        "description_ru": "Бронирование ж/д билетов",
        "description_en": "Book train tickets",
    },
    "buses": {
        "name_ru": "Автобусы",
        "name_en": "Buses",
        "icon": "🚌",
        "description_ru": "Междугородние автобусы",
        "description_en": "Intercity bus tickets",
    },
    "cruises": {
        "name_ru": "Круизы",
        "name_en": "Cruises",
        "icon": "🚢",
        "description_ru": "Морские и речные круизы",
        "description_en": "Sea and river cruises",
    },
    "sanatoriums": {
        "name_ru": "Санатории",
        "name_en": "Sanatoriums",
        "icon": "♨️",
        "description_ru": "Санаторно-курортное лечение",
        "description_en": "Health resorts and sanatoriums",
    },
    "camping": {
        "name_ru": "Турбазы",
        "name_en": "Camping",
        "icon": "⛺",
        "description_ru": "Турбазы и кемпинги",
        "description_en": "Campgrounds and eco-lodges",
    },
    "luggage": {
        "name_ru": "Хранение багажа",
        "name_en": "Luggage Storage",
        "icon": "🧳",
        "description_ru": "Хранение багажа в городе",
        "description_en": "Store luggage in the city",
    },
    "yacht": {
        "name_ru": "Аренда яхт",
        "name_en": "Yacht Rental",
        "icon": "⛵",
        "description_ru": "Аренда яхт и катеров",
        "description_en": "Rent yachts and boats",
    },
    "compensation": {
        "name_ru": "Компенсации",
        "name_en": "Compensation",
        "icon": "💰",
        "description_ru": "Возмещение за задержку рейса",
        "description_en": "Flight delay compensation",
    },
    "portal": {
        "name_ru": "Путешествия",
        "name_en": "Travel",
        "icon": "🌐",
        "description_ru": "Портал путешествий",
        "description_en": "Travel portal",
    },
    "marketplace": {
        "name_ru": "Маркетплейс",
        "name_en": "Marketplace",
        "icon": "🛒",
        "description_ru": "Покупки и товары для путешествий",
        "description_en": "Shopping and travel gear",
    },
}

# ---------------------------------------------------------------------------
# SERVICE LISTS BY CATEGORY — for easy lookup
# ---------------------------------------------------------------------------

def get_services_by_category(category):
    """Return list of service dicts for a given category."""
    return [s for s in SERVICE_REGISTRY.values() if s["category"] == category]

def get_services_by_lang(lang):
    """Return list of services available in a given language."""
    return [s for s in SERVICE_REGISTRY.values() if lang in s["langs"]]

def get_service_by_name(name):
    """Lookup service by any of its aliases (case-insensitive)."""
    name_lower = name.lower()
    for svc in SERVICE_REGISTRY.values():
        if name_lower in [a.lower() for a in svc["aliases"]]:
            return svc
    return None

def get_link_for_service(service_key):
    """Get the tpx tracking link for a service by key."""
    svc = SERVICE_REGISTRY.get(service_key)
    return svc["url"] if svc else None

# ---------------------------------------------------------------------------
# LINK GENERATORS — dynamic links with tracking parameters
# ---------------------------------------------------------------------------

def hotels_link(city_name_en):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3772&source_type=link&type=click'
        f'&campaign_id=101&trs=search_hotels_{city_name_en.lower().replace(" ", "_")}'
    )

def hotels_link_named(hotel_name_en, city_name_en="", checkin="", checkout=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3772&source_type=link&type=click'
        f'&campaign_id=101&trs=search_hotels_{hotel_name_en.lower().replace(" ", "_")}'
    )

def flights_link(origin="MOW", destination=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3770&source_type=link&type=click'
        f'&campaign_id=100&trs=search_flights_{origin}_{destination}'
    )

def tours_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3774&source_type=link&type=click'
        f'&campaign_id=103&trs=search_tours_{city_name_en.lower().replace(" ", "_")}'
    )

def insurance_link():
    return SERVICE_REGISTRY["cherehapa"]["url"]

def excursions_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=4137&source_type=link&type=click'
        f'&campaign_id=131&trs=search_excursions_{city_name_en.lower().replace(" ", "_")}'
    )

def transfers_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3782&source_type=link&type=click'
        f'&campaign_id=112&trs=search_transfers_{city_name_en.lower().replace(" ", "_")}'
    )

def esim_link():
    return SERVICE_REGISTRY["airalo"]["url"]

def car_rental_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3780&source_type=link&type=click'
        f'&campaign_id=111&trs=search_car_rental_{city_name_en.lower().replace(" ", "_")}'
    )

def tickets_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3801&source_type=link&type=click'
        f'&campaign_id=116&trs=search_tickets_{city_name_en.lower().replace(" ", "_")}'
    )

def trains_link():
    return SERVICE_REGISTRY["tutu"]["url"]

def buses_link():
    return SERVICE_REGISTRY["unitiki"]["url"]

def cruises_link():
    return SERVICE_REGISTRY["kruizonline"]["url"]

def sanatorium_link():
    return SERVICE_REGISTRY["sanatory"]["url"]

def luggage_link():
    return SERVICE_REGISTRY["radicalstorage"]["url"]

def yacht_link():
    return SERVICE_REGISTRY["searadar"]["url"]

# ---------------------------------------------------------------------------
# AFFILIATE HTML BLOCKS — templates for in-article CTAs
# ---------------------------------------------------------------------------

AFFILIATE_HTML = {
    # Hotels
    "hotels": '<div class="affiliate-block"><p>Проверьте актуальные цены на Hotellook:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">сравнить цены на отели в {city}</a></div>',
    "hotels_en": '<div class="affiliate-block"><p>Check real-time prices on Hotellook:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">compare hotel prices in {city}</a></div>',
    "hotels_es": '<div class="affiliate-block"><p>Compara precios de hoteles en tiempo real:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">comparar precios de hoteles en {city}</a></div>',
    # Flights
    "flights": '<div class="affiliate-block"><p>Сравните цены на авиабилеты:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">посмотреть билеты в {city}</a></div>',
    "flights_en": '<div class="affiliate-block"><p>Compare flight prices:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">check flights to {city}</a></div>',
    "flights_es": '<div class="affiliate-block"><p>Compara precios de vuelos:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">buscar vuelos a {city}</a></div>',
    # Tours
    "tours": '<div class="affiliate-block"><p>Подберите тур с лучшими ценами:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">подобрать тур в {city}</a></div>',
    "tours_en": '<div class="affiliate-block"><p>Find the best tour deals:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">find tours to {city}</a></div>',
    "tours_es": '<div class="affiliate-block"><p>Encuentra los mejores tours:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">buscar tours en {city}</a></div>',
    # Insurance
    "insurance": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">оформить страховку</a>',
    "insurance_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">get travel insurance</a>',
    "insurance_es": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">contratar seguro de viaje</a>',
    # Excursions
    "excursions": '<div class="affiliate-block"><p>Забронируйте экскурсию заранее:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">экскурсии в {city}</a></div>',
    "excursions_en": '<div class="affiliate-block"><p>Book excursions in advance:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">excursions in {city}</a></div>',
    "excursions_es": '<div class="affiliate-block"><p>Reserva excursiones con antelación:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">excursiones en {city}</a></div>',
    # Transfers
    "transfers": '<div class="affiliate-block"><p>Закажите трансфер из аэропорта:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">трансфер в {city}</a></div>',
    "transfers_en": '<div class="affiliate-block"><p>Book an airport transfer:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">airport transfer to {city}</a></div>',
    "transfers_es": '<div class="affiliate-block"><p>Reserva un transfer desde el aeropuerto:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">transfer aeropuerto a {city}</a></div>',
    # eSIM
    "esim": '<div class="affiliate-block"><p>Купите eSIM для поездки:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">eSIM для {city}</a></div>',
    "esim_en": '<div class="affiliate-block"><p>Get an eSIM for your trip:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">eSIM for {city}</a></div>',
    "esim_es": '<div class="affiliate-block"><p>Consigue una eSIM para tu viaje:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">eSIM para {city}</a></div>',
    # Car Rental
    "car_rental": '<div class="affiliate-block"><p>Арендуйте автомобиль:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">аренда авто в {city}</a></div>',
    "car_rental_en": '<div class="affiliate-block"><p>Rent a car:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">car rental in {city}</a></div>',
    "car_rental_es": '<div class="affiliate-block"><p>Alquila un coche:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">alquilar coche en {city}</a></div>',
    # Tickets
    "tickets": '<div class="affiliate-block"><p>Купите билеты онлайн:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">билеты в {city}</a></div>',
    "tickets_en": '<div class="affiliate-block"><p>Book tickets online:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">tickets in {city}</a></div>',
    "tickets_es": '<div class="affiliate-block"><p>Compra entradas online:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">entradas en {city}</a></div>',
    # Trains
    "trains": '<div class="affiliate-block"><p>Купите ж/д билеты:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">билеты на поезд</a></div>',
    "trains_en": '<div class="affiliate-block"><p>Book train tickets:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">train tickets</a></div>',
    "trains_es": '<div class="affiliate-block"><p>Compra billetes de tren:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">billetes de tren</a></div>',
    # Buses
    "buses": '<div class="affiliate-block"><p>Купите билеты на автобус:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">автобусы</a></div>',
    "buses_en": '<div class="affiliate-block"><p>Book bus tickets:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">bus tickets</a></div>',
    "buses_es": '<div class="affiliate-block"><p>Compra billetes de autobús:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">billetes de autobús</a></div>',
    # Sanatoriums (RU only)
    "sanatoriums": '<div class="affiliate-block"><p>Подберите санаторий:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">санатории</a></div>',
}

PLACEHOLDERS = {
    "{hotels_placeholder}": "hotels",
    "{flights_placeholder}": "flights",
    "{tours_placeholder}": "tours",
    "{excursions_placeholder}": "excursions",
    "{transfers_placeholder}": "transfers",
    "{esim_placeholder}": "esim",
    "{car_rental_placeholder}": "car_rental",
    "{insurance_placeholder}": "insurance",
    "{tickets_placeholder}": "tickets",
    "{trains_placeholder}": "trains",
    "{buses_placeholder}": "buses",
    "{sanatoriums_placeholder}": "sanatoriums",
}

# ---------------------------------------------------------------------------
# BACKWARD-COMPAT: flat list for publisher.py linkify_services()
# ---------------------------------------------------------------------------

SERVICES_FLAT = [(svc["name"], svc["url"]) for svc in SERVICE_REGISTRY.values()]
