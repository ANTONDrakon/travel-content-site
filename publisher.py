import os
import re
import json
from pathlib import Path

MARKER = "736226"

SERVICES = [
    ("Aviasales", f"https://tp.media/click?shmarker={MARKER}&promo_id=3770&source_type=link&type=click&campaign_id=100&trs=aviasales"),
    ("Hotellook", f"https://tp.media/click?shmarker={MARKER}&promo_id=3772&source_type=link&type=click&campaign_id=101&trs=hotellook"),
    ("Booking.com", f"https://tp.media/click?shmarker={MARKER}&promo_id=3776&source_type=link&type=click&campaign_id=108&trs=booking"),
    ("Booking", f"https://tp.media/click?shmarker={MARKER}&promo_id=3776&source_type=link&type=click&campaign_id=108&trs=booking"),
    ("Agoda", f"https://tp.media/click?shmarker={MARKER}&promo_id=3779&source_type=link&type=click&campaign_id=110&trs=agoda"),
    ("GetYourGuide", f"https://tp.media/click?shmarker={MARKER}&promo_id=3798&source_type=link&type=click&campaign_id=115&trs=getyourguide"),
    ("Viator", f"https://tp.media/click?shmarker={MARKER}&promo_id=3775&source_type=link&type=click&campaign_id=107&trs=viator"),
    ("Kiwitaxi", f"https://tp.media/click?shmarker={MARKER}&promo_id=3782&source_type=link&type=click&campaign_id=112&trs=kiwitaxi"),
    ("Airalo", f"https://tp.media/click?shmarker={MARKER}&promo_id=3803&source_type=link&type=click&campaign_id=118&trs=airalo"),
    ("DiscoverCars", f"https://tp.media/click?shmarker={MARKER}&promo_id=3780&source_type=link&type=click&campaign_id=111&trs=discovercars"),
    ("Localrent", f"https://tp.media/click?shmarker={MARKER}&promo_id=3783&source_type=link&type=click&campaign_id=113&trs=localrent"),
    ("Tiqets", f"https://tp.media/click?shmarker={MARKER}&promo_id=3801&source_type=link&type=click&campaign_id=116&trs=tiqets"),
    ("Klook", f"https://tp.media/click?shmarker={MARKER}&promo_id=3797&source_type=link&type=click&campaign_id=120&trs=klook"),
    ("Kiwi.com", f"https://tp.media/click?shmarker={MARKER}&promo_id=3799&source_type=link&type=click&campaign_id=114&trs=kiwicom"),
    ("Trip.com", f"https://tp.media/click?shmarker={MARKER}&promo_id=3802&source_type=link&type=click&campaign_id=119&trs=tripcom"),
    ("Compensair", f"https://tp.media/click?shmarker={MARKER}&promo_id=3800&source_type=link&type=click&campaign_id=117&trs=compensair"),
    ("Cherehapa", f"https://tp.media/click?shmarker={MARKER}&promo_id=3773&source_type=link&type=click&campaign_id=102&trs=insurance"),
    ("12Go", f"https://tp.media/click?shmarker={MARKER}&promo_id=4127&source_type=link&type=click&campaign_id=121&trs=12go"),
]

def linkify_services(body):
    for name, url in SERVICES:
        if name in body:
            pattern = re.compile(r'(?<!["\'>])(' + re.escape(name) + r')(?!["\'<])')
            replacement = f'<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-link">{name}</a>'
            body = pattern.sub(replacement, body, count=1)
    return body

PRICE_CONVERSIONS = {
    "$": "≈ ₽{rub}", "€": "≈ ₽{rub}", "AED": "≈ ₽{rub}",
    "฿": "≈ ₽{rub}", "THB": "≈ ₽{rub}", "₺": "≈ ₽{rub}",
    "TRY": "≈ ₽{rub}", "EGP": "≈ ₽{rub}", "¥": "≈ ₽{rub}",
    "CNY": "≈ ₽{rub}", "IDR": "≈ ₽{rub}",
}

def convert_prices_to_rub(body, lang="ru"):
    if lang == "ru":
        def dollar_convert(m):
            amt = m.group(1)
            try:
                rub = int(float(amt.replace(",", "")) * 95)
                return f"₽{rub:,} (≈ ${amt})".replace(",", " ")
            except:
                return m.group(0)
        body = re.sub(r'\$(\d[\d,.]*)', dollar_convert, body)

        def euro_convert(m):
            amt = m.group(1)
            try:
                rub = int(float(amt.replace(",", "")) * 103)
                return f"₽{rub:,} (≈ €{amt})".replace(",", " ")
            except:
                return m.group(0)
        body = re.sub(r'€(\d[\d,.]*)', euro_convert, body)
    else:
        def dollar_add_rub(m):
            amt = m.group(1)
            try:
                rub = int(float(amt.replace(",", "")) * 95)
                return f"${amt} (≈ ₽{rub:,})".replace(",", " ")
            except:
                return m.group(0)
        body = re.sub(r'\$(\d[\d,.]*)', dollar_add_rub, body)
    return body

def inject_maldives_qr(body, country_slug):
    if country_slug != "maldives":
        return body
    qr_text = '<p><strong>📱 Важно:</strong> Перед вылетом на Мальдивы заполните декларацию IMUGA на сайте <strong>imuga.immigration.gov.mv</strong> и получите QR-код — без него вас не посадят на рейс. Если не хотите разбираться самостоятельно — я помогаю своим туристам с оформлением.</p>'
    visa_pattern = re.compile(r'(<h2[^>]*>.*?(?:виза|visa|документ|document).*?</h2>.*?)(<h2)', re.IGNORECASE | re.DOTALL)
    match = visa_pattern.search(body)
    if match:
        insert_pos = match.end(1)
        body = body[:insert_pos] + qr_text + body[insert_pos:]
    return body

from jinja2 import Environment, FileSystemLoader, select_autoescape


SITE_DIR = Path(__file__).parent / "site"
TEMPLATES_DIR = SITE_DIR / "templates"
OUTPUT_DIR = Path(__file__).parent / "docs"
CONTENT_DIR = Path(__file__).parent / "content"


env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)
env.globals["site_url"] = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")
env.globals["formspree_id"] = "xnjyjnnd"
env.globals["enumerate"] = enumerate


COUNTRY_IMAGES = {
    "turkey": "https://as2.ftcdn.net/jpg/08/45/68/41/1000_F_845684119_DjY0EbNBL7XLomrwnYvTEZU9LvUYfi3U.jpg",
    "thailand": "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=1200&q=80",
    "egypt": "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200&q=80",
    "uae": "https://plantravel.ru/Upload/images/other/php8loD6m.jpg",
    "indonesia": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&q=80",
    "china": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
    "maldives": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1200&q=80",
}

CITY_IMAGES = {
    "istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=80",
    "antalya": "https://youtravel.me/upload/medialibrary/73c/g4ldxc78rw7lit49arn32dfdexy36p78.jpg",
    "alanya": "https://images.unsplash.com/photo-1597074866923-dc0589150358?w=800&q=80",
    "bodrum": "https://avatars.mds.yandex.net/i?id=01074de7a85624d1ae3164b00d594852_l-5319522-images-thumbs&n=13",
    "cappadocia": "https://irecommend.ru/sites/default/files/imagecache/copyright1/user-images/173895/RfFySz3wO2UvbxBAH17Q.jpg",
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80",
    "phuket": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "pattaya": "https://images.unsplash.com/photo-1506665531195-3566af2b4dfa?w=800&q=80",
    "koh-samui": "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=800&q=80",
    "krabi": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800&q=80",
    "sharm-el-sheikh": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Sharm_El_Sheikh_-_panoramio_%2811%29.jpg",
    "hurghada": "https://avatars.mds.yandex.net/get-altay/14296560/2a000001925220f1ecd9241e93837a93b267/orig",
    "cairo": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    "luxor": "https://hurghadaexcurs.com/wp-content/uploads/2024/05/EXCURSION_TO_LUXOR_2_DAYS_INDIVIDUALLY_FROM_HURGHADA_main.jpg",
    "marsa-alam": "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "abu-dhabi": "https://ic.pics.livejournal.com/pantv/14908973/12182338/12182338_original.jpg",
    "sharjah": "https://i.pinimg.com/originals/b9/a2/23/b9a223075cf4d19a0c15c66dfaedac01.jpg",
    "ras-al-khaimah": "https://fs.tonkosti.ru/sized/c800x800/8d/ut/8dutekrq5hwc0kwgw4gs4wooc.jpg",
    "fujairah": "https://fs.tonkosti.ru/tonkosti/table_img/g142/9d9d/266410251.jpg",
    "ubud": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
    "kuta": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "seminyak": "https://images.unsplash.com/photo-1539367628448-4bc5c9d171c8?w=800&q=80",
    "canggu": "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?w=800&q=80",
    "nusa-dua": "https://images.unsplash.com/photo-1573790387438-4da905039392?w=800&q=80",
    "sanya": "https://avatars.mds.yandex.net/get-altay/6322664/2a000001907e422c5f8766638ecbd3745e61/orig",
    "haikou": "https://russian.cgtn.com/news/2025-09-30/1972981899919007745/b0142e6b-dec8-41a1-b227-e290b3f07083.png",
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "shanghai": "https://images.unsplash.com/photo-1538428494232-9c0d8a3ab403?w=800&q=80",
    "xian": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800&q=80",
    "male": "https://cs.pikabu.ru/post_img/big/2013/03/30/2/1364602604_1624085555.jpg",
    "hulhumale": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/70683603.jpg?k=a299869c220804e8410738b0afa5f166be86303ebfda1b3b989e7fb65128a3c5&o=",
    "maafushi": "https://vectorme.ru/wp-content/uploads/2023/03/ostrov-maafushi-2048x1091.png",
    "dhigurah": "https://i.ytimg.com/vi/p6XxR6fn8xA/maxresdefault.jpg",
    "thulusdhoo": "https://www.hotels-maldives.net/data/Photos/OriginalPhoto/7901/790145/790145394.JPEG",
    "resort-islands": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
}


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_city_image(city_slug):
    return CITY_IMAGES.get(city_slug, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")


def get_country_image(country_slug):
    return COUNTRY_IMAGES.get(country_slug, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&q=80")


def get_country_emoji(slug):
    emojis = {
        "turkey": "🇹🇷", "thailand": "🇹🇭", "egypt": "🇪🇬",
        "uae": "🇦🇪", "indonesia": "🇮🇩", "china": "🇨🇳", "maldives": "🇲🇻",
    }
    return emojis.get(slug, "🌍")


def build_home_page(lang):
    from config.destinations import DESTINATIONS

    countries_data = []
    for slug, country in DESTINATIONS.items():
        countries_data.append({
            "slug": slug,
            "name_ru": country["name_ru"],
            "name_en": country["name_en"],
            "emoji": get_country_emoji(slug),
            "image": get_country_image(slug),
            "cities": country["cities"],
            "cities_count": len(country["cities"]),
            "guides_count": len(country["cities"]) * 5,
        })

    template = env.get_template("home.html")
    html = template.render(
        lang=lang,
        countries=countries_data,
        alternate_url="index.html",
        breadcrumbs=None,
    )

    out = OUTPUT_DIR / lang / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_destination_page(country_slug, lang):
    from config.destinations import DESTINATIONS
    from agents.seo_optimizer import get_url_slug
    from config.affiliates import insurance_link

    country = DESTINATIONS.get(country_slug)
    if not country:
        print(f"  Unknown country: {country_slug}")
        return

    from config.country_data import COUNTRY_DATA, AGENT_PHOTO, AGENT_PHOTOS

    country_data = COUNTRY_DATA.get(country_slug, {})

    icons = {
        "guide": "📖", "hotels": "🏨", "flights": "✈️",
        "attractions": "🏛", "seasons": "☀️",
    }
    if lang == "ru":
        labels = {
            "guide": "Путеводитель", "hotels": "Отели", "flights": "Авиабилеты",
            "attractions": "Достопримечательности", "seasons": "Сезоны и погода",
        }
    else:
        labels = {
            "guide": "Travel Guide", "hotels": "Hotels", "flights": "Flights",
            "attractions": "Attractions", "seasons": "Seasons & Weather",
        }

    all_articles = {}
    for city_slug, city_data in country["cities"].items():
        city_articles = []
        for ct_slug in ["guide", "hotels", "flights", "attractions", "seasons"]:
            url_slug = get_url_slug(ct_slug, city_slug, lang)
            city_articles.append({
                "url": url_slug,
                "label": labels.get(ct_slug, ct_slug),
                "icon": icons.get(ct_slug, "📄"),
            })
        all_articles[city_slug] = city_articles

    cities_with_images = {}
    for city_slug, city_data in country["cities"].items():
        cities_with_images[city_slug] = {
            "name_ru": city_data["name_ru"],
            "name_en": city_data["name_en"],
            "articles": all_articles[city_slug],
            "image": get_city_image(city_slug),
        }

    city_names_list = [c["name_en"] if lang == "en" else c["name_ru"] for c in country["cities"].values()]

    city_descriptions = {
        "istanbul": "Город на двух континентах: дворцы, мечети, базары. Культурная столица страны.",
        "antalya": "Средиземноморский курорт: пляжи, All Inclusive, Старый город. Универсальный выбор.",
        "alanya": "Бюджетный курорт с крепостью и пляжем Клеопатры. Отличный сервис за разумные деньги.",
        "bodrum": "Эгейский курорт европейского стиля: марина, белые дома, ночная жизнь.",
        "cappadocia": "Лунный пейзаж, воздушные шары, пещерные отели. Уникальный регион.",
        "bangkok": "Мегаполис контрастов: храмы, небоскрёбы, стритфуд. Ворота в Юго-Восточную Азию.",
        "phuket": "Крупнейший остров Таиланда: пляжи, дайвинг, ночная жизнь.",
        "pattaya": "Курортный город с активной ночной жизнью. Бюджетно, весело, близко к Бангкоку.",
        "koh-samui": "Остров с кокосовыми рощами и спа. Спокойный, семейный, живописный.",
        "krabi": "Провинция с карстовыми скалами и изумрудным морем. Для любителей природы.",
        "sharm-el-sheikh": "Дайверская столица Красного моря. Кораллы, рыбы, заповедник Рас-Мохаммед.",
        "hurghada": "Самый доступный курорт Египта. Пляжный отдых, дайвинг, экскурсии.",
        "cairo": "Мегаполис у пирамид. Гизы, Каирский музей, базар Хан-эль-Халили.",
        "luxor": "Древние Фивы: Долина царей, Карнакский храм. Музей под открытым небом.",
        "marsa-alam": "Уединённый дайверский рай на юге. Дюгони, нетронутые рифы.",
        "dubai": "Город будущего: небоскрёбы, шопинг, развлечения. Самый популярный эмират.",
        "abu-dhabi": "Столица ОАЭ: культура, Лувр, мечеть шейха Зайда. Спокойный и респектабельный.",
        "sharjah": "Культурная столица: музеи, heritage-районы. Самый строгий, но бюджетный.",
        "fujairah": "Единственный эмират на Индийском океане. Дайвинг, снорклинг, горы Хаджар.",
        "ras-al-khaimah": "Природа и приключения: гора Джебель-Джейс, мангровые заросли, уединение.",
        "ubud": "Духовное сердце Бали: рисовые террасы, йога, храмы. Для творческих натур.",
        "kuta": "Пляжный и серф-центр Бали. Бюджетно, шумно, весело.",
        "seminyak": "Богемный район Бали: модные кафе, бутики, закатные бары.",
        "canggu": "Хипстерский серф-район Бали: кофе, бассейны, коворкинги.",
        "nusa-dua": "Элитный анклав Бали: люксовые курорты, гольф, белый песок.",
        "sanya": "Тропический рай Хайнаня: пальмы, пляжи, бухты. Китайские Гавайи.",
        "haikou": "Столица Хайнаня: колониальная архитектура, вулканические парки.",
        "beijing": "Великая столица: Запретный город, Великая стена, хутуны.",
        "shanghai": "Футуристический мегаполис: Вайтань, небоскрёбы Пудуна.",
        "xian": "Древняя столица: Терракотовая армия, мусульманский квартал.",
        "male": "Столица Мальдив: коралловая мечеть, рыбный рынок, отправная точка.",
        "maafushi": "Бюджетный локальный остров: бикини-бич, экскурсии, гестхаусы.",
        "hulhumale": "Искусственный остров: широкие пляжи, новый аэропорт.",
        "thulusdhoo": "Сёрф-остров: волны, кокосовая фабрика, аутентичный быт.",
        "dhigurah": "Длинный песчаный остров: китовые акулы, дайвинг, уединение.",
        "istanbul_en": "City on two continents: palaces, mosques, bazaars. Cultural capital.",
        "antalya_en": "Mediterranean resort: beaches, All Inclusive, Old Town. Universal choice.",
        "alanya_en": "Budget resort with castle and Cleopatra Beach. Great value for money.",
        "bodrum_en": "Aegean resort with European flair: marina, white houses, nightlife.",
        "cappadocia_en": "Lunar landscape, balloons, cave hotels. Unique region of Turkey.",
        "bangkok_en": "Megacity of contrasts: temples, skyscrapers, street food. Gateway to SE Asia.",
        "phuket_en": "Thailand's largest island: beaches, diving, nightlife. For everyone.",
        "pattaya_en": "Resort city with vibrant nightlife. Budget-friendly, close to Bangkok.",
        "koh-samui_en": "Island with coconut groves and spas. Relaxed, family-friendly, scenic.",
        "krabi_en": "Province with karst cliffs and emerald sea. For nature lovers.",
        "sharm-el-sheikh_en": "Diving capital of the Red Sea. Corals, fish, Ras Mohammed Reserve.",
        "hurghada_en": "Egypt's most affordable resort. Beach vacation, diving, excursions.",
        "cairo_en": "Megacity by the pyramids. Giza, Egyptian Museum, Khan El Khalili.",
        "luxor_en": "Ancient Thebes: Valley of Kings, Karnak Temple. Open-air museum.",
        "marsa-alam_en": "Secluded diving paradise in the south. Dugongs, pristine reefs.",
        "dubai_en": "City of the future: skyscrapers, shopping, entertainment. Most popular emirate.",
        "abu-dhabi_en": "Capital of UAE: culture, Louvre, Sheikh Zayed Mosque. Calm and respectable.",
        "sharjah_en": "Cultural capital: museums, heritage districts. Strictest but affordable.",
        "fujairah_en": "Only emirate on Indian Ocean. Diving, snorkeling, Hajar Mountains.",
        "ras-al-khaimah_en": "Nature & adventure: Jebel Jais, mangroves, total seclusion.",
        "ubud_en": "Spiritual heart of Bali: rice terraces, yoga, temples. For creatives.",
        "kuta_en": "Beach and surf center of Bali. Budget, loud, fun.",
        "seminyak_en": "Bohemian Bali: trendy cafes, boutiques, sunset bars.",
        "canggu_en": "Hipster surf area: coffee, pools, co-working spaces.",
        "nusa-dua_en": "Elite Bali enclave: luxury resorts, golf, white sand.",
        "sanya_en": "Hainan's tropical paradise: palms, beaches, bays. China's Hawaii.",
        "haikou_en": "Hainan's capital: colonial architecture, volcanic parks, spa.",
        "beijing_en": "Great capital: Forbidden City, Great Wall, hutongs.",
        "shanghai_en": "Futuristic megacity: Bund waterfront, Pudong skyscrapers.",
        "xian_en": "Ancient capital: Terracotta Army, Muslim Quarter, city wall.",
        "male_en": "Maldives capital: coral mosque, fish market, departure point.",
        "maafushi_en": "Budget local island: bikini beach, excursions, guesthouses.",
        "hulhumale_en": "Artificial island: wide beaches, new airport, modern.",
        "thulusdhoo_en": "Surf island: waves, coconut factory, authentic island life.",
        "dhigurah_en": "Long sandbank island: whale sharks, diving, total seclusion.",
    }

    for city_slug in cities_with_images:
        desc_key = f"{city_slug}_en" if lang == "en" else city_slug
        cities_with_images[city_slug]["desc"] = city_descriptions.get(desc_key, "")

    template = env.get_template("destination-rich.html")

    html = template.render(
        lang=lang,
        country=country,
        cities=cities_with_images,
        city_names=city_names_list,
        articles_count=len(country["cities"]) * 5,
        hero_image=get_country_image(country_slug),
        insurance_link=insurance_link(),
        data=country_data,
        agent_photo=AGENT_PHOTO,
        agent_photos=AGENT_PHOTOS,
        alternate_url=f"{country_slug}/index.html",
        breadcrumbs=[
            {"label": "Home" if lang == "en" else "Главная", "url": f"/{lang}/index.html"},
            {"label": country["name_en"] if lang == "en" else country["name_ru"],
             "url": f"/{lang}/{country_slug}/index.html"},
        ],
    )

    out = OUTPUT_DIR / lang / country_slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_article_page(country_slug, city_slug, content_type, lang):
    from config.destinations import DESTINATIONS
    from agents.seo_optimizer import get_url_slug, build_seo_meta, generate_schema_article, generate_schema_faq, generate_faq
    from config.prompts import CONTENT_TYPES
    from agents.image_injector import inject_hotel_images, inject_attraction_images

    country = DESTINATIONS.get(country_slug)
    if not country:
        return

    city = country["cities"].get(city_slug)
    if not city:
        return

    city_name = city["name_ru"] if lang == "ru" else city["name_en"]
    country_name = country["name_ru"] if lang == "ru" else country["name_en"]

    content_type_slug = get_url_slug(content_type, city_slug, lang)

    article_json = CONTENT_DIR / lang / country_slug / f"{content_type_slug}.json"
    if not article_json.exists():
        print(f"  Missing: {article_json}")
        return

    article_data = load_json(article_json)
    if not article_data:
        return

    body = article_data.get("body", "")
    if content_type == "hotels":
        body = inject_hotel_images(body)
    if content_type == "attractions":
        body = inject_attraction_images(body)

    body = linkify_services(body)
    body = convert_prices_to_rub(body, lang)
    body = inject_maldives_qr(body, country_slug)

    import re as _re
    body = _re.sub(r'<h1[^>]*>.*?</h1>\s*', '', body, count=1)

    article_meta = {
        "title": article_data.get("title", ""),
        "meta_description": article_data.get("meta_description", ""),
        "h1": article_data.get("h1", ""),
        "body": body,
    }

    seo = build_seo_meta(article_meta, city_slug, country_slug, content_type, lang)

    faq_data = generate_faq(city_name, content_type, lang)

    alt_url = f"{country_slug}/{content_type_slug}.html"
    en_alt_slug = get_url_slug(content_type, city_slug, "en")
    ru_alt_slug = get_url_slug(content_type, city_slug, "ru")
    url = f"/{lang}/{country_slug}/{content_type_slug}.html"

    schema_article = generate_schema_article(seo, city_name, country_name, url, lang)
    schema_faq = generate_schema_faq(faq_data)

    city_name_for_breadcrumb = city["name_ru"] if lang == "ru" else city["name_en"]

    breadcrumbs = [
        {"label": "Home" if lang == "en" else "Главная", "url": f"/{lang}/index.html"},
        {"label": country_name, "url": f"/{lang}/{country_slug}/index.html"},
        {"label": city_name_for_breadcrumb, "url": f"/{lang}/{country_slug}/{content_type_slug}.html"},
    ]

    from agents.seo_optimizer import generate_schema_breadcrumbs
    schema_breadcrumbs = generate_schema_breadcrumbs(breadcrumbs)
    schema_data = [schema_article, schema_faq, schema_breadcrumbs]

    related = []
    for ct_slug, ct_info in CONTENT_TYPES.items():
        if ct_slug != content_type:
            rel_slug = get_url_slug(ct_slug, city_slug, lang)
            related.append({
                "url": f"{country_slug}/{rel_slug}.html",
                "title": city_name_for_breadcrumb,
                "type": ct_info["category_ru"] if lang == "ru" else ct_info["category_en"],
            })

    hero_image = get_city_image(city_slug)

    template = env.get_template("article.html")
    html = template.render(
        lang=lang,
        article={
            "title": seo["title"],
            "meta_description": seo["meta_description"],
            "h1": seo["h1"],
            "body": article_meta["body"],
        },
        faq=faq_data,
        related=related,
        canonical=seo["canonical"],
        en_alt_url=f"{country_slug}/{en_alt_slug}.html",
        ru_alt_url=f"{country_slug}/{ru_alt_slug}.html",
        schema_data=schema_data,
        breadcrumbs=breadcrumbs,
        alternate_url=alt_url,
        hero_image=hero_image,
    )

    out = OUTPUT_DIR / lang / country_slug / f"{content_type_slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_index_redirect():
    html = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta http-equiv="refresh" content="0;url=/en/index.html">
<title>TravelHub</title><script>window.location.href="/en/index.html";</script></head>
<body><p>Redirecting to <a href="/en/index.html">TravelHub</a>...</p></body></html>"""
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")


def build_all():
    print("\n=== Building site ===\n")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    for lang in ["ru", "en"]:
        print(f"\n[{lang.upper()}] Building home page...")
        build_home_page(lang)

    for country_slug in DESTINATIONS:
        for lang in ["ru", "en"]:
            print(f"\n[{lang.upper()}] Building {country_slug}...")
            build_destination_page(country_slug, lang)
            for city_slug in DESTINATIONS[country_slug]["cities"]:
                for ct_slug in CONTENT_TYPES:
                    build_article_page(country_slug, city_slug, ct_slug, lang)

    build_index_redirect()
    print("\n=== Site built ===\n")


if __name__ == "__main__":
    build_all()
