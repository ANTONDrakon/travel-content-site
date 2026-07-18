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
    "hotels": '<div class="affiliate-block"><p>Проверьте актуальные цены на Hotellook:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">сравнить цены на отели в {city}</a></div>',
    "hotels_en": '<div class="affiliate-block"><p>Check real-time prices on Hotellook:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">compare hotel prices in {city}</a></div>',
    "flights": '<div class="affiliate-block"><p>Сравните цены на авиабилеты:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">посмотреть билеты в {city}</a></div>',
    "flights_en": '<div class="affiliate-block"><p>Compare flight prices:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">check flights to {city}</a></div>',
    "tours": '<div class="affiliate-block"><p>Подберите тур с лучшими ценами:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">подобрать тур в {city}</a></div>',
    "tours_en": '<div class="affiliate-block"><p>Find the best tour deals:</p><a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">find tours to {city}</a></div>',
    "insurance": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">оформить страховку</a>',
    "insurance_en": '<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">get travel insurance</a>',
}

PLACEHOLDERS = {
    "{hotels_placeholder}": "hotels",
    "{flights_placeholder}": "flights",
    "{tours_placeholder}": "tours",
}
