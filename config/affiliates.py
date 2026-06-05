import os

MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "736226")

def hotels_link(city_name_en):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3772&source_type=link&type=click'
        f'&campaign_id=101&trs=search_hotels_{city_name_en.lower().replace(" ", "_")}'
    )

def hotels_link_named(hotel_name_en, city_name_en="", checkin="", checkout=""):
    url = (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3772&source_type=link&type=click'
        f'&campaign_id=101&trs=search_hotels_{hotel_name_en.lower().replace(" ", "_")}'
    )
    return url

def flights_link(origin="MOW", destination=""):
    url = (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3770&source_type=link&type=click'
        f'&campaign_id=100&trs=search_flights_{origin}_{destination}'
    )
    return url

def tours_link(city_name_en=""):
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3774&source_type=link&type=click'
        f'&campaign_id=103&trs=search_tours_{city_name_en.lower().replace(" ", "_")}'
    )

def insurance_link():
    return (
        f'https://tp.media/click?shmarker={MARKER}'
        f'&promo_id=3773&source_type=link&type=click'
        f'&campaign_id=102&trs=travel_insurance'
    )

AFFILIATE_HTML = {
    "hotels": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🔍 Найти отели в {city} на Hotellook</a>',
    "hotels_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🔍 Find hotels in {city} on Hotellook</a>',
    "flights": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">✈️ Найти дешёвые билеты в {city} на Aviasales</a>',
    "flights_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">✈️ Find cheap flights to {city} on Aviasales</a>',
    "tours": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🏝 Подобрать тур в {city}</a>',
    "tours_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🏝 Book a tour to {city}</a>',
    "insurance": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🛡 Оформить страховку для путешествия</a>',
    "insurance_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="affiliate-link">🛡 Get travel insurance</a>',
}

PLACEHOLDERS = {
    "{hotels_placeholder}": "hotels",
    "{flights_placeholder}": "flights",
    "{tours_placeholder}": "tours",
}
