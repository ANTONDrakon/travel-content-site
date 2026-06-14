import os
import re
import json
from pathlib import Path

MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "736226")

SERVICES = [
    ("Aviasales", f"https://tp.media/click?shmarker={MARKER}&promo_id=3770&source_type=link&type=click&campaign_id=100&trs=aviasales"),
    ("Hotellook", f"https://tp.media/click?shmarker={MARKER}&promo_id=3772&source_type=link&type=click&campaign_id=101&trs=hotellook"),
    ("Booking.com", f"https://tp.media/click?shmarker={MARKER}&promo_id=3776&source_type=link&type=click&campaign_id=108&trs=booking"),
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

# Exchange rates to RUB — auto-fetched from API, with fallback defaults
DEFAULT_RATES = {"$": 95, "€": 103, "₺": 3.5, "฿": 2.7, "¥": 13.3, "AED": 25.9, "EGP": 1.9, "IDR": 0.006, "MVR": 6.2}

def _fetch_exchange_rates():
    """Fetch live exchange rates to RUB from free API. Falls back to defaults."""
    import urllib.request, json as _json
    try:
        # Try open.er-api.com (free, no key required)
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        req = urllib.request.Request(url, headers={"User-Agent": "TravelHub/1.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = _json.loads(resp.read().decode())
        usd_base = data.get("rates", {})
        # Get RUB per USD
        rub_per_usd = usd_base.get("RUB", DEFAULT_RATES["$"])
        rates = {
            "$": rub_per_usd,
            "€": rub_per_usd / usd_base.get("EUR", 0.92) if usd_base.get("EUR") else DEFAULT_RATES["€"],
            "₺": rub_per_usd / usd_base.get("TRY", 31.0) if usd_base.get("TRY") else DEFAULT_RATES["₺"],
            "฿": rub_per_usd / usd_base.get("THB", 35.0) if usd_base.get("THB") else DEFAULT_RATES["฿"],
            "¥": rub_per_usd / usd_base.get("CNY", 7.2) if usd_base.get("CNY") else DEFAULT_RATES["¥"],
            "AED": rub_per_usd / usd_base.get("AED", 3.67) if usd_base.get("AED") else DEFAULT_RATES["AED"],
            "EGP": rub_per_usd / usd_base.get("EGP", 30.0) if usd_base.get("EGP") else DEFAULT_RATES["EGP"],
            "IDR": rub_per_usd / usd_base.get("IDR", 16000.0) if usd_base.get("IDR") else DEFAULT_RATES["IDR"],
            "MVR": rub_per_usd / usd_base.get("MVR", 15.42) if usd_base.get("MVR") else DEFAULT_RATES["MVR"],
        }
        print(f"  Exchange rates fetched live: $1 = {rub_per_usd} RUB")
        return rates
    except Exception as e:
        print(f"  Warning: could not fetch live rates ({e}), using defaults")
        return dict(DEFAULT_RATES)

RATES_TO_RUB = _fetch_exchange_rates()

def _clean_amount(s):
    return s.strip().replace(",", "").replace(" ", "")

def convert_prices_to_rub(body, lang="ru"):
    """Convert raw currency amounts to RUB (RU) or USD (EN) with local currency in parentheses.
    Skips already-converted patterns (those already containing both currencies)."""
    if lang == "ru":
        # RU: RUB main + (local in parentheses)
        def _ru_convert(m):
            amt = _clean_amount(m.group(1))
            sym = m.group(0)[0]
            try:
                rate = RATES_TO_RUB.get(sym, 1)
                rub = int(float(amt) * rate)
                if sym == "$":
                    return f"₽{rub:,} (${amt})".replace(",", " ")
                elif sym == "€":
                    return f"₽{rub:,} (€{amt})".replace(",", " ")
                elif sym == "₺":
                    return f"₽{rub:,} ({amt} ₺)".replace(",", " ")
                elif sym == "฿":
                    return f"₽{rub:,} ({amt} ฿)".replace(",", " ")
                elif sym == "¥":
                    return f"₽{rub:,} ({amt} ¥)".replace(",", " ")
                else:
                    return f"₽{rub:,} ({amt} {sym})".replace(",", " ")
            except:
                return m.group(0)

        # Only convert if NOT already in a (parentheses) — skip pre-converted
        for sym in ["$", "€", "₺", "฿", "¥"]:
            escaped = re.escape(sym)
            body = re.sub(r'(?<![\(\d])' + escaped + r'(\d[\d,.]*(?:\s*\d{3})*)', _ru_convert, body)

        # AED/EGP/IDR/MVR with number + code format
        for code, sym_icon in [("AED", "AED"), ("EGP", "EGP"), ("IDR", "IDR"), ("MVR", "MVR")]:
            def _make_conv(c, si):
                def _f(m):
                    amt = _clean_amount(m.group(1))
                    try:
                        rub = int(float(amt) * RATES_TO_RUB.get(c, 1))
                        return f"₽{rub:,} ({amt} {si})".replace(",", " ")
                    except:
                        return m.group(0)
                return _f
            body = re.sub(r'(?<![\(\d])(\d[\d,.]*(?:\s*\d{3})*)\s*' + code, _make_conv(code, sym_icon), body)
    else:
        # EN: USD main + (local in parentheses)
        usd_rate = RATES_TO_RUB["$"]
        def _en_convert(m):
            amt = _clean_amount(m.group(1))
            sym = m.group(0)[0]
            try:
                rub = float(amt) * RATES_TO_RUB.get(sym, 1)
                usd = rub / usd_rate
                if sym == "$":
                    return f"${amt}"
                elif sym == "€":
                    return f"${usd:,.0f} (€{amt})".replace(",", " ")
                elif sym == "₺":
                    return f"${usd:,.0f} ({amt} ₺)".replace(",", " ")
                elif sym == "฿":
                    return f"${usd:,.0f} ({amt} ฿)".replace(",", " ")
                elif sym == "¥":
                    return f"${usd:,.0f} ({amt} ¥)".replace(",", " ")
                else:
                    return f"${usd:,.0f} ({amt} {sym})".replace(",", " ")
            except:
                return m.group(0)

        for sym in ["$", "€", "₺", "฿", "¥"]:
            escaped = re.escape(sym)
            # For EN, skip $ if already in parentheses (pre-converted)
            if sym == "$":
                body = re.sub(r'(?<![\(\d])' + escaped + r'(\d[\d,.]*(?:\s*\d{3})*)', lambda m: _en_convert(m) if "₽" not in m.group(0) else m.group(0), body)
            else:
                body = re.sub(r'(?<![\(\d])' + escaped + r'(\d[\d,.]*(?:\s*\d{3})*)', _en_convert, body)

        for code, sym_icon in [("AED", "AED"), ("EGP", "EGP"), ("IDR", "IDR"), ("MVR", "MVR")]:
            def _make_en_conv(c, si):
                def _f(m):
                    amt = _clean_amount(m.group(1))
                    try:
                        rub = float(amt) * RATES_TO_RUB.get(c, 1)
                        usd = rub / usd_rate
                        return f"${usd:,.0f} ({amt} {si})".replace(",", " ")
                    except:
                        return m.group(0)
                return _f
            body = re.sub(r'(?<![\(\d])(\d[\d,.]*(?:\s*\d{3})*)\s*' + code, _make_en_conv(code, sym_icon), body)

    return body

def inject_disclaimer(body, lang="ru"):
    """Add price disclaimer at the end of article body."""
    if lang == "ru":
        notice = '<div class="partner-block" style="margin-top:40px;"><h4>⚠️ Важно: о ценах</h4><p style="font-size:14px;color:var(--charcoal);line-height:1.7;">Все цены в статье являются <strong>ориентировочными</strong> и основаны на средних рыночных данных. Актуальные цены всегда проверяйте на сайтах партнёров (Aviasales, Hotellook, Booking, Agoda и др.). Курсы валют обновляются автоматически, но могут отличаться от курсов вашего банка.</p></div>'
    else:
        notice = '<div class="partner-block" style="margin-top:40px;"><h4>⚠️ Important: About Prices</h4><p style="font-size:14px;color:var(--charcoal);line-height:1.7;">All prices in this article are <strong>approximate estimates</strong> based on typical market rates. Always check current prices on partner booking sites (Aviasales, Hotellook, Booking, Agoda, etc.). Exchange rates are updated automatically but may differ from your bank\'s rates.</p></div>'
    return body + notice

def inject_photo_disclaimer(body, lang="ru"):
    """Add photo disclaimer after the first image block."""
    if lang == "ru":
        notice = '<p style="font-size:12px;color:var(--meta);margin-top:-16px;margin-bottom:24px;font-style:italic;">📷 Изображения отелей носят иллюстративный характер и могут не соответствовать фактическому виду отеля.</p>'
    else:
        notice = '<p style="font-size:12px;color:var(--meta);margin-top:-16px;margin-bottom:24px;font-style:italic;">📷 Hotel images are for illustration purposes only and may not reflect the actual property.</p>'
    # Insert after first </figure> or <img> tag
    body = re.sub(r'(<(?:figure|img)[^>]*>)', r'\1' + notice, body, count=1)
    return body

def inject_maldives_qr(body, country_slug, lang="ru"):
    if country_slug != "maldives":
        return body
    if lang == "ru":
        qr_text = '<p><strong>📱 Важно:</strong> Перед вылетом на Мальдивы заполните декларацию IMUGA на сайте <strong>imuga.immigration.gov.mv</strong> и получите QR-код — без него вас не посадят на рейс. Если не хотите разбираться самостоятельно — обратитесь к нашему турагенту, мы поможем с оформлением.</p>'
    else:
        qr_text = '<p><strong>📱 Important:</strong> Before flying to Maldives, fill out the IMUGA declaration at <strong>imuga.immigration.gov.mv</strong> and get a QR code — without it you will not be allowed to board your flight. If you need help, contact our travel agent for assistance with the process.</p>'
    visa_pattern = re.compile(r'(<h2[^>]*>.*?(?:виза|visa|документ|document).*?</h2>.*?)(<h2)', re.IGNORECASE | re.DOTALL)
    match = visa_pattern.search(body)
    if match:
        insert_pos = match.end(1)
        body = body[:insert_pos] + qr_text + body[insert_pos:]
    return body

def sanitize_agent_references(body):
    """Remove remaining first-person agent persona references from AI-generated content."""
    body = re.sub(r'Я, Валентина Туркова[ ,]+', 'Я, ваш гид, ', body)
    body = re.sub(r'я, Валентина Туркова[ ,]+', 'я, ваш гид, ', body)
    body = re.sub(r'Валентина Туркова', 'ваш гид', body)
    body = re.sub(r'я Валентина[ ,]+', 'я ', body)
    body = re.sub(r'"Valentina, [^"]*"', '"Traveler, "', body)
    body = re.sub(r'Валентина[,\s]+(?!Туркова)', 'гид ', body)
    body = re.sub(r'Valentina Turkova', 'your guide', body)
    body = re.sub(r"I'm Valentina[,\s]+", "I'm ", body)
    body = re.sub(r'my tourists', 'travelers', body, flags=re.IGNORECASE)
    body = re.sub(r'my travelers', 'travelers', body, flags=re.IGNORECASE)
    # Remove common first-person impersonation patterns
    body = re.sub(r'я отправила более? \d+', 'мы отправили более', body, flags=re.IGNORECASE)
    body = re.sub(r'я отправил[ао]? \d+', 'мы отправили', body, flags=re.IGNORECASE)
    body = re.sub(r'за \d+ лет работы агентом', 'по опыту нашей команды', body)
    body = re.sub(r'мои туристы', 'наши путешественники', body)
    body = re.sub(r'моих туристов', 'наших путешественников', body)
    body = re.sub(r'моим туристам', 'нашим путешественникам', body)
    body = re.sub(r'моя особая любовь', 'особое место', body)
    body = re.sub(r'моя наценка', 'наценка', body, flags=re.IGNORECASE)
    body = re.sub(r'моей наценк', 'наценк', body, flags=re.IGNORECASE)
    body = re.sub(r'\[моя наценка[^\]]*\]', '', body)
    body = re.sub(r'\(с моей наценкой[^)]*\)', '', body)
    body = re.sub(r'\(с учётом моей наценки[^)]*\)', '', body)
    body = re.sub(r'мои клиенты', 'наши клиенты', body)
    body = re.sub(r'моих клиентов', 'наших клиентов', body)
    body = re.sub(r'своими туристами', 'путешественниками', body)
    body = re.sub(r'своих туристов', 'путешественников', body)
    body = re.sub(r'I\'ve sent dozens of travelers', 'Many travelers have', body)
    body = re.sub(r'I\'ve sent dozens', 'Many have', body)
    body = re.sub(r"I've sent dozens", 'Many have', body)
    body = re.sub(r"I'm about to spill all my secrets", "here are some tips", body)
    body = re.sub(r"spill all my secrets", "share some tips", body)
    body = re.sub(r'my clients', 'travelers', body)
    body = re.sub(r'my secret', 'a tip', body, flags=re.IGNORECASE)
    body = re.sub(r'my special', 'a special', body, flags=re.IGNORECASE)
    return body


# ─── Editor enhancements (migrated from editor_agent.py) ───

def _editor_enhance_body(body, lang="ru"):
    """Apply editorial enhancements: diversify templates, break long sentences."""
    import random
    
    if lang == "ru":
        why_patterns = [
            (r'\bПочему стоит поехать именно сейчас\?', 'Стоит ли ехать прямо сейчас?'),
            (r'\bПочему стоит поехать именно в 2026 году\?', 'Чем хорош 2026 год для поездки?'),
            (r'\bПочему стоит поехать\?', 'В чём главные причины поехать?'),
            (r'\bПочему стоит поехать сюда\?', 'Что делает это место особенным?'),
        ]
        for pattern, replacement in why_patterns:
            body = re.sub(pattern, replacement, body)
    
    if lang == "en":
        en_why_patterns = [
            (r'\bWhy visit \w+ in 2026\?', 'What makes this a great destination in 2026?'),
            (r'\bWhy visit in 2026\?', 'Why is 2026 the year to visit?'),
            (r'\bWhy visit \w+\?', 'What draws travelers here?'),
        ]
        for pattern, replacement in en_why_patterns:
            body = re.sub(pattern, replacement, body)
    
    long_sentence_patterns = [
        (r'(Вы сможете [^.]{60,}?), (а\s+\w+)', r'\1. \2'),
        (r'(Здесь каждый найдет что-то свое: [^.]{50,}?), (а\s+\w+)', r'\1. \2'),
        (r'(you can [^.]{60,}?), (and\s+\w+)', r'\1. \2'),
        (r'(You can [^.]{60,}?), (and\s+\w+)', r'\1. \2'),
    ]
    for pattern, replacement in long_sentence_patterns:
        body = re.sub(pattern, replacement, body)
    
    sensory_ru = {
        'никогда не спит': ['живёт полной жизнью', 'пульсирует энергией', 'никогда не затихает'],
        'предлагает путешественникам': ['дарит гостям', 'открывает перед путешественниками'],
    }
    sensory_en = {
        'is a city of superlatives': ['is a destination that defies expectations', 'sets new standards at every turn'],
        'offers an unparalleled': ['delivers an unmatched', 'provides a world-class'],
    }
    sensory_map = sensory_ru if lang == "ru" else sensory_en
    for old, alts in sensory_map.items():
        random.seed(hash(body) % 10000)
        body = body.replace(old, random.choice(alts), 1)
    
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
    "turkey": "/assets/countries/turkey.webp",
    "thailand": "/assets/countries/thailand.webp",
    "egypt": "/assets/countries/egypt.webp",
    "uae": "/assets/countries/uae.webp",
    "indonesia": "/assets/countries/indonesia.webp",
    "china": "/assets/countries/china.webp",
    "maldives": "/assets/countries/maldives.webp",
}

CITY_IMAGES = {
    "istanbul": "/assets/cities/istanbul.webp",
    "antalya": "/assets/cities/antalya.webp",
    "alanya": "/assets/cities/alanya.webp",
    "bodrum": "/assets/cities/bodrum.webp",
    "cappadocia": "/assets/cities/cappadocia.webp",
    "bangkok": "/assets/cities/bangkok.webp",
    "phuket": "/assets/cities/phuket.webp",
    "pattaya": "/assets/cities/pattaya.webp",
    "koh-samui": "/assets/cities/koh-samui.webp",
    "krabi": "/assets/cities/krabi.webp",
    "sharm-el-sheikh": "/assets/cities/sharm-el-sheikh.webp",
    "hurghada": "/assets/cities/hurghada.webp",
    "cairo": "/assets/cities/cairo.webp",
    "luxor": "/assets/cities/luxor.webp",
    "marsa-alam": "/assets/cities/marsa-alam.webp",
    "dubai": "/assets/cities/dubai.webp",
    "abu-dhabi": "/assets/cities/abu-dhabi.webp",
    "sharjah": "/assets/cities/sharjah.webp",
    "ras-al-khaimah": "/assets/cities/ras-al-khaimah.webp",
    "fujairah": "/assets/cities/fujairah.webp",
    "ubud": "/assets/cities/ubud.webp",
    "kuta": "/assets/cities/kuta.webp",
    "seminyak": "/assets/cities/seminyak.webp",
    "canggu": "/assets/cities/canggu.webp",
    "nusa-dua": "/assets/cities/nusa-dua.webp",
    "sanya": "/assets/cities/sanya.webp",
    "haikou": "/assets/cities/haikou.webp",
    "beijing": "/assets/cities/beijing.webp",
    "shanghai": "/assets/cities/shanghai.webp",
    "xian": "/assets/cities/xian.webp",
    "male": "/assets/cities/male.webp",
    "hulhumale": "/assets/cities/hulhumale.webp",
    "maafushi": "/assets/cities/maafushi.webp",
    "dhigurah": "/assets/cities/dhigurah.webp",
    "thulusdhoo": "/assets/cities/thulusdhoo.webp",
    "resort-islands": "/assets/cities/resort-islands.webp",
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
    from agents.image_injector import inject_hotel_carousels, inject_attraction_images

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
        body = inject_hotel_carousels(body, country_slug, city_slug, lang)
    if content_type == "attractions":
        body = inject_attraction_images(body)

    body = linkify_services(body)
    body = convert_prices_to_rub(body, lang)
    body = sanitize_agent_references(body)
    body = _editor_enhance_body(body, lang)
    body = inject_disclaimer(body, lang)
    body = inject_photo_disclaimer(body, lang)
    body = inject_maldives_qr(body, country_slug, lang)

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
