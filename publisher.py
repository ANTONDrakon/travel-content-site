import os
import re
import json
from pathlib import Path
from config.affiliates import SERVICE_REGISTRY, SERVICES_FLAT

MARKER = os.getenv("TRAVELPAYOUTS_MARKER", "736226")

# Backward-compatible flat list: [(name, url), ...]
SERVICES = SERVICES_FLAT

def linkify_services(body):
    """Auto-link partner service names in article text using the centralized registry."""
    for svc in SERVICE_REGISTRY.values():
        for alias in svc["aliases"]:
            if alias in body:
                pattern = re.compile(r'(?<!["\'>])(' + re.escape(alias) + r')(?!["\'<])')
                replacement = f'<a href="{svc["url"]}" target="_blank" rel="nofollow sponsored" class="partner-link">{alias}</a>'
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

RATES_TO_RUB = None  # Lazy-loaded on first use

def _get_rates():
    global RATES_TO_RUB
    if RATES_TO_RUB is None:
        RATES_TO_RUB = _fetch_exchange_rates()
    return RATES_TO_RUB

def _clean_amount(s):
    return s.strip().replace(",", "").replace(" ", "")

def convert_prices_to_rub(body, lang="ru"):
    """Convert raw currency amounts to RUB (RU) or USD (EN) with local currency in parentheses.
    Skips already-converted patterns (those already containing both currencies)."""
    if lang == "ru":
        # RU: RUB main + (local in parentheses)
        rates = _get_rates()
        def _ru_convert(m):
            amt = _clean_amount(m.group(1))
            sym = m.group(0)[0]
            try:
                rate = rates.get(sym, 1)
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
            except (ValueError, KeyError, TypeError):
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
                        rub = int(float(amt) * rates.get(c, 1))
                        return f"₽{rub:,} ({amt} {si})".replace(",", " ")
                    except (ValueError, KeyError, TypeError):
                        return m.group(0)
                return _f
            body = re.sub(r'(?<![\(\d])(\d[\d,.]*(?:\s*\d{3})*)\s*' + code, _make_conv(code, sym_icon), body)
    else:
        # EN: USD main + (local in parentheses)
        rates = _get_rates()
        usd_rate = rates["$"]
        def _en_convert(m):
            amt = _clean_amount(m.group(1))
            sym = m.group(0)[0]
            try:
                rub = float(amt) * rates.get(sym, 1)
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
            except (ValueError, KeyError, TypeError):
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
                        rub = float(amt) * rates.get(c, 1)
                        usd = rub / usd_rate
                        return f"${usd:,.0f} ({amt} {si})".replace(",", " ")
                    except (ValueError, KeyError, TypeError):
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

def inject_china_entry_info(body, country_slug, lang="ru"):
    if country_slug != "china":
        return body
    if lang == "ru":
        qr_text = '<p><strong>📱 Важно для Китая:</strong> Для въезда в Китай требуется QR-код здоровья (WeChat или Alipay). Заполните декларацию здоровья за 24 часа до вылета. Также потребуется загранпаспорт с визой (оформляется через туроператора). Для Хайнаня — безвизовый въезд до 30 дней через туроператора.</p>'
    else:
        qr_text = '<p><strong>📱 Important for China:</strong> A health QR code (via WeChat or Alipay) is required for entry. Fill out the health declaration within 24 hours before departure. A passport with visa is required (processed via tour operator). Hainan: visa-free entry for up to 30 days via tour operator.</p>'
    visa_pattern = re.compile(r'(<h[23][^>]*>.*?(?:виза|visa|документ|document|правила въезда|entry rules).*?</h[23]>.*?)(<h[23])', re.IGNORECASE | re.DOTALL)
    match = visa_pattern.search(body)
    if match:
        insert_pos = match.end(1)
        body = body[:insert_pos] + qr_text + body[insert_pos:]
    return body


def inject_maldives_qr(body, country_slug, lang="ru"):
    if country_slug != "maldives":
        return body
    if lang == "ru":
        qr_text = '<p><strong>📱 Важно:</strong> Перед вылетом на Мальдивы заполните декларацию IMUGA на сайте <strong>imuga.immigration.gov.mv</strong> и получите QR-код — без него вас не посадят на рейс. Виза по прибытии — бесплатно, до 30 дней. Если не хотите разбираться самостоятельно — обратитесь к нашему турагенту, мы поможем с оформлением.</p>'
    else:
        qr_text = '<p><strong>📱 Important:</strong> Before flying to Maldives, fill out the IMUGA declaration at <strong>imuga.immigration.gov.mv</strong> and get a QR code — without it you will not be allowed to board your flight. Free visa on arrival for up to 30 days. If you need help, contact our travel agent for assistance with the process.</p>'
    visa_pattern = re.compile(r'(<h[23][^>]*>.*?(?:виза|visa|документ|document).*?</h[23]>.*?)(<h[23])', re.IGNORECASE | re.DOTALL)
    match = visa_pattern.search(body)
    if match:
        insert_pos = match.end(1)
        body = body[:insert_pos] + qr_text + body[insert_pos:]
    return body

def sanitize_agent_references(body):
    """Clean up AI-generated persona artifacts while preserving the Valentina Turkova brand.

    Valentina Turkova is a real travel agent — keep her name.
    Only fix obviously fake AI-persona patterns.
    """
    # Fix fake first-person claims (AI over-claims)
    body = re.sub(r'я отправила более? \d+', 'мы отправили более', body, flags=re.IGNORECASE)
    body = re.sub(r'я отправил[ао]? \d+', 'мы отправили', body, flags=re.IGNORECASE)
    body = re.sub(r'за \d+ лет работы агентом', 'по опыту нашей команды', body)

    # Fix possessive patterns that sound AI-generated
    body = re.sub(r'мои туристы', 'наши путешественники', body)
    body = re.sub(r'моих туристов', 'наших путешественников', body)
    body = re.sub(r'моим туристам', 'нашим путешественникам', body)
    body = re.sub(r'мои клиенты', 'наши клиенты', body)
    body = re.sub(r'моих клиентов', 'наших клиентов', body)
    body = re.sub(r'своими туристами', 'путешественниками', body)
    body = re.sub(r'своих туристов', 'путешественников', body)

    # Remove onca markup artifacts
    body = re.sub(r'моя особая любовь', 'особое место', body)
    body = re.sub(r'\[моя наценка[^\]]*\]', '', body)
    body = re.sub(r'\(с моей наценкой[^)]*\)', '', body)
    body = re.sub(r'\(с учётом моей наценки[^)]*\)', '', body)

    # English AI-persona fixes
    body = re.sub(r"I'm about to spill all my secrets", "here are some tips", body)
    body = re.sub(r"spill all my secrets", "share some tips", body)
    body = re.sub(r'my secret', 'a tip', body, flags=re.IGNORECASE)

    # Fix "Я, Валентина" and "I'm Valentina" patterns in article body
    body = re.sub(r'Я,\s*Валентина[^.]*?,\s*', '', body)
    body = re.sub(r'я,\s*Валентина[^.]*?,\s*', '', body)
    body = re.sub(r"I'm Valentina[^.]*?,\s*", "", body)
    body = re.sub(r"I, Valentina[^.]*?,\s*", "", body)

    # Fix "С любовью к приключениям, Валентина" sign-offs
    body = re.sub(r'С любовью к приключениям,?\s*Валентина\.?\s*[^<]*', '', body)
    body = re.sub(r'С любовью,?\s*Валентина\.?\s*[^<]*', '', body)
    body = re.sub(r'With love,?\s*Valentina\.?\s*[^<]*', '', body)

    # Fix "Валентина, ты гений" and similar quotes
    body = re.sub(r'«Валентина,?[^»]*»', '', body)
    body = re.sub(r'"Valentina[^"]*"', '', body)

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
from urllib.parse import urlparse as _urlparse
_env_root = _urlparse(os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")).path.rstrip("/")
env.globals["root"] = _env_root
env.globals["formspree_id"] = "xnjyjnnd"
env.globals["enumerate"] = enumerate

# Analytics configuration
env.globals["analytics_enabled"] = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
env.globals["yandex_metrika_id"] = os.getenv("YANDEX_METRIKA_ID", None)
env.globals["google_analytics_id"] = os.getenv("GOOGLE_ANALYTICS_ID", None)

# reCAPTCHA configuration (spam protection for forms)
env.globals["recaptcha_site_key"] = os.getenv("RECAPTCHA_SITE_KEY", None)

# Brevo newsletter configuration
# Get your form URL from Brevo > Contacts > Forms > Create a form
env.globals["brevo_form_url"] = os.getenv("BREVO_FORM_URL", None)

# Dynamic copyright year
from datetime import date
env.globals["current_year"] = str(date.today().year)

# Centralized destinations list for forms, footer, and navigation
# Single source of truth — used in base.html, home.html, and all templates
DESTINATIONS_LIST = [
    # Russia
    {"slug": "russia", "name_ru": "Россия", "name_en": "Russia", "group": "russia"},
    {"slug": "baikal", "name_ru": "Байкал", "name_en": "Lake Baikal", "group": "russia"},
    {"slug": "altai", "name_ru": "Алтай", "name_en": "Altai", "group": "russia"},
    {"slug": "karelia", "name_ru": "Карелия", "name_en": "Karelia", "group": "russia"},
    {"slug": "dagestan", "name_ru": "Дагестан", "name_en": "Dagestan", "group": "russia"},
    {"slug": "kamchatka", "name_ru": "Камчатка", "name_en": "Kamchatka", "group": "russia"},
    {"slug": "mineral-vody", "name_ru": "Кавказские Минеральные Воды", "name_en": "Caucasian Mineral Waters", "group": "russia"},
    {"slug": "kavkaz", "name_ru": "Кавказ", "name_en": "Caucasus", "group": "russia"},
    {"slug": "vladivostok", "name_ru": "Владивосток", "name_en": "Vladivostok", "group": "russia"},
    # International
    {"slug": "turkey", "name_ru": "Турция", "name_en": "Turkey", "group": "international"},
    {"slug": "thailand", "name_ru": "Таиланд", "name_en": "Thailand", "group": "international"},
    {"slug": "egypt", "name_ru": "Египет", "name_en": "Egypt", "group": "international"},
    {"slug": "uae", "name_ru": "ОАЭ", "name_en": "UAE", "group": "international"},
    {"slug": "indonesia", "name_ru": "Индонезия", "name_en": "Indonesia", "group": "international"},
    {"slug": "china", "name_ru": "Китай", "name_en": "China", "group": "international"},
    {"slug": "maldives", "name_ru": "Мальдивы", "name_en": "Maldives", "group": "international"},
    {"slug": "sri-lanka", "name_ru": "Шри-Ланка", "name_en": "Sri Lanka", "group": "international"},
    {"slug": "montenegro", "name_ru": "Черногория", "name_en": "Montenegro", "group": "international"},
    {"slug": "vietnam", "name_ru": "Вьетнам", "name_en": "Vietnam", "group": "international"},
    {"slug": "georgia", "name_ru": "Грузия", "name_en": "Georgia", "group": "international"},
    {"slug": "cyprus", "name_ru": "Кипр", "name_en": "Cyprus", "group": "international"},
    {"slug": "oman", "name_ru": "Оман", "name_en": "Oman", "group": "international"},
]

env.globals["destinations_list"] = DESTINATIONS_LIST
env.globals["russia_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "russia"]
env.globals["international_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "international"]


COUNTRY_IMAGES = {
    "russia": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1200&q=80",
    "baikal": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=1200&q=80",
    "altai": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
    "karelia": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80",
    "dagestan": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=1200&q=80",
    "kamchatka": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
    "mineral-vody": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1200&q=80",
    "kavkaz": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
    "vladivostok": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=1200&q=80",
    "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80",
    "thailand": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1200&q=80",
    "egypt": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80",
    "uae": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80",
    "indonesia": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1200&q=80",
    "china": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
    "maldives": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1200&q=80",
    "sri-lanka": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=1200&q=80",
    "montenegro": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=1200&q=80",
    "vietnam": "https://images.unsplash.com/photo-1528127269322-539801943592?w=1200&q=80",
    "georgia": "https://images.unsplash.com/photo-1565008576549-57569a49371d?w=1200&q=80",
    "cyprus": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1200&q=80",
    "oman": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?w=1200&q=80",
}

CITY_IMAGES = {
    # Turkey
    "istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=80",
    "antalya": "https://images.unsplash.com/photo-1591994843349-f415f2e6e1a0?w=800&q=80",
    "bodrum": "https://images.unsplash.com/photo-1591994843349-f415f2e6e1a0?w=800&q=80",
    "cappadocia": "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?w=800&q=80",
    # Thailand
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80",
    "phuket": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "pattaya": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "koh-samui": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "krabi": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    # Egypt
    "sharm-el-sheikh": "https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=800&q=80",
    "hurghada": "https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=800&q=80",
    "cairo": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    "luxor": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    "marsa-alam": "https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=800&q=80",
    # UAE
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "abu-dhabi": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "sharjah": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "ras-al-khaimah": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "fujairah": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    # Indonesia
    "ubud": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "kuta": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "seminyak": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "canggu": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "nusa-dua": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    # China
    "sanya": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "haikou": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "shanghai": "https://images.unsplash.com/photo-1546412414-e1885e5109b5?w=800&q=80",
    "xian": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    # Maldives
    "male": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "maafushi": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "hulhumale": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "thulusdhoo": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "dhigurah": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "resort-islands": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    # Sri Lanka
    "colombo": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=800&q=80",
    "bentota": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=800&q=80",
    "unawatuna": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=800&q=80",
    "sigiriya": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=800&q=80",
    # Montenegro
    "budva": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=800&q=80",
    "kotor": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=800&q=80",
    "tivat": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=800&q=80",
    "herceg-novi": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=800&q=80",
    # Vietnam
    "da-nang": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80",
    "phu-quoc": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80",
    "nha-trang": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80",
    "hanoi": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80",
    # Georgia
    "tbilisi": "https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800&q=80",
    "batumi": "https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800&q=80",
    "kutaisi": "https://images.unsplash.com/photo-1565008576549-57569a49371d?w=800&q=80",
    # Cyprus
    "limassol": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
    "ayia-napa": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
    "paphos": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
    # Oman
    "muscat": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?w=800&q=80",
    "salalah": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?w=800&q=80",
    "musandam": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?w=800&q=80",
    # Russia
    "moscow": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80",
    "saint-petersburg": "https://images.unsplash.com/photo-1556610930-e515011324f3?w=800&q=80",
    "sochi": "https://images.unsplash.com/photo-1548636800-4abe7e58658e?w=800&q=80",
    "kaliningrad": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&q=80",
    "kazan": "https://images.unsplash.com/photo-1570710891163-6d3b5c47248b?w=800&q=80",
    # Baikal
    "irkutsk": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=800&q=80",
    "listvyanka": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=800&q=80",
    "olkhon": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=800&q=80",
    # Altai
    "gorno-altaysk": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    "chemyal": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    "akkem": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    # Karelia
    "petrozavodsk": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80",
    "sortavala": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80",
    "kizhi": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&q=80",
    # Dagestan
    "makhachkala": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=800&q=80",
    "derbent": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=800&q=80",
    "kizlyar": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=800&q=80",
    # Kamchatka
    "petropavlovsk-kamchatsky": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    "paratunka": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    # Mineral Waters
    "pyatigorsk": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
    "kislovodsk": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
    "essentuki": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
    # Vladivostok
    "vladivostok-city": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80",
    "russky-island": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80",
    # Caucasus
    "dombay": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    "elbrus": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    "kislovodsk-c": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
}


def load_json(path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Warning: Corrupted JSON file {path.name}: {e}")
        return {}
    except Exception as e:
        print(f"  Warning: Could not read {path.name}: {e}")
        return {}


def get_city_image(city_slug):
    path = CITY_IMAGES.get(city_slug, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")
    if path.startswith("/") and _env_root:
        return _env_root + path
    return path


def get_country_image(country_slug):
    path = COUNTRY_IMAGES.get(country_slug, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200&q=80")
    if path.startswith("/") and _env_root:
        return _env_root + path
    return path


def get_country_emoji(slug):
    emojis = {
        "russia": "🇷🇺", "baikal": "💎", "altai": "🏔", "karelia": "🌲",
        "dagestan": "⛰️", "kamchatka": "🌋", "mineral-vody": "♨️", "vladivostok": "⚓",
        "turkey": "🇹🇷", "thailand": "🇹🇭", "egypt": "🇪🇬",
        "uae": "🇦🇪", "indonesia": "🇮🇩", "china": "🇨🇳", "maldives": "🇲🇻",
        "sri-lanka": "🇱🇰", "montenegro": "🇲🇪", "vietnam": "🇻🇳",
        "georgia": "🇬🇪", "cyprus": "🇨🇾", "oman": "🇴🇲",
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
        # Russian destinations
        "moscow": "Столица России: Кремль, Красная площадь, Третьяковка. Сердце страны.",
        "saint-petersburg": "Северная Венеция: Эрмитаж, белые ночи, дворцы и разводные мосты.",
        "sochi": "Курортное сердце Черноморья: пляжи, Олимпиада, Красная Поляна.",
        "kaliningrad": "Русская Европа: янтарь, форты, балтийские пляжи.",
        "kazan": "Столица Татарстана: Кремль, мечеть Кул-Шариф, восточный колорит.",
        "irkutsk": "Врата к Байкалу: деревянные дома, озёра, тайга.",
        "listvyanka": "Посёлок на берегу Байкала: музей озера, промысел, свежая рыба.",
        "olkhon": "Остров в сердце Байкала: шаманские места, скалы, пляжи.",
        "gorno-altaysk": "Горная столица Алтая: природа, горы, реки.",
        "chemyal": "Живописное ущелье на Чемале: Аккемский водопад, мосты.",
        "akkem": "Лагерь у подножия Белухи: треккинг, горные озёра.",
        "petrozavodsk": "Столица Карелии: озёра, национальные парки, традиции.",
        "sortavala": "Город у Ладожского озера: крепость, парки, острова.",
        "kizhi": "Остров-музей: Преображенская церковь, деревянное зодчество.",
        "makhachkala": "Столица Дагестана: горы, базары, гостеприимство.",
        "derbent": "Древнейший город России: Нарын-кала, старый город.",
        "kizlyar": "Ворота Дагестана: виноделие, казачья культура.",
        "petropavlovsk-kamchatsky": "Столица Камчатки: вулканы, гейзеры, медведи.",
        "paratunka": "Курорт с горячими источниками: термальные ванны.",
        "pyatigorsk": "Столица КМВ: серные источники, Лермонтовские места.",
        "kislovodsk": "Город-курорт: Нарзанная галерея, долина роз.",
        "essentuki": "Минеральные воды: питьевые источники, парки.",
        "vladivostok-city": "Порт на Тихом океане: мосты, бухты, Азиатско-Тихоокеанская конференция.",
        "russky-island": "Остров у Владивостока: мост, пляжи, парки.",
        # English
        "moscow_en": "Capital of Russia: Kremlin, Red Square, Tretyakov Gallery. Heart of the country.",
        "saint-petersburg_en": "Northern Venice: Hermitage, White Nights, palaces and drawbridges.",
        "sochi_en": "Black Sea resort: beaches, Olympics, Krasnaya Polyana skiing.",
        "kaliningrad_en": "Russian Europe: amber, forts, Baltic beaches.",
        "kazan_en": "Capital of Tatarstan: Kremlin, Kul-Sharif mosque, Eastern flair.",
        "irkutsk_en": "Gateway to Baikal: wooden houses, lakes, taiga.",
        "listvyanka_en": "Village on Lake Baikal: museum, fishing, fresh omul.",
        "olkhon_en": "Island in the heart of Baikal: shamanic sites, cliffs, beaches.",
        "gorno-altaysk_en": "Mountain capital of Altai: nature, rivers, peaks.",
        "chemyal_en": "Scenic Chemal gorge: Akkem waterfall, bridges.",
        "akkem_en": "Camp at the foot of Belukha: trekking, mountain lakes.",
        "petrozavodsk_en": "Capital of Karelia: lakes, national parks, traditions.",
        "sortavala_en": "City by Lake Ladoga: fortress, parks, islands.",
        "kizhi_en": "Museum island: Transfiguration Church, wooden architecture.",
        "makhachkala_en": "Capital of Dagestan: mountains, bazaars, hospitality.",
        "derbent_en": "Russia's oldest city: Naryn-Kala fortress, old town.",
        "kizlyar_en": "Gateway to Dagestan: winemaking, Cossack culture.",
        "petropavlovsk-kamchatsky_en": "Capital of Kamchatka: volcanoes, geysers, bears.",
        "paratunka_en": "Resort with hot springs: thermal baths.",
        "pyatigorsk_en": "Capital of Caucasian Mineral Waters: sulfur springs, Lermontov heritage.",
        "kislovodsk_en": "Spa city: Narzan gallery, rose valley.",
        "essentuki_en": "Mineral waters: drinking springs, parks.",
        "vladivostok-city_en": "Port on the Pacific: bridges, bays, APEC venue.",
        "russky-island_en": "Island near Vladivostok: bridge, beaches, parks.",
        # Caucasus
        "dombay": "Горнолыжный курорт: канатная дорога, горы, отели у подножия.",
        "elbrus": "Высочайшая точка Европы: канатные дороги, ледники, треккинг.",
        "kislovodsk-c": "Курортный город: Нарзанная галерея, парки, долина роз.",
        "dombay_en": "Ski resort: cable car, mountains, hotels at the foot.",
        "elbrus_en": "Highest point in Europe: cable cars, glaciers, trekking.",
        "kislovodsk-c_en": "Spa city: Narzan Gallery, parks, rose valley.",
    }

    for city_slug in cities_with_images:
        desc_key = f"{city_slug}_en" if lang == "en" else city_slug
        cities_with_images[city_slug]["desc"] = city_descriptions.get(desc_key, "")

    template = env.get_template("destination-rich.html")

    og_images = {
        "russia": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1200&q=80",
        "baikal": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=1200&q=80",
        "altai": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
        "karelia": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80",
        "dagestan": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=1200&q=80",
        "kamchatka": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
        "mineral-vody": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1200&q=80",
        "vladivostok": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=1200&q=80",
        "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80",
        "thailand": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1200&q=80",
        "egypt": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80",
        "uae": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80",
        "indonesia": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1200&q=80",
        "china": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        "maldives": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1200&q=80",
    }
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
        og_image=og_images.get(country_slug, ""),
    )

    out = OUTPUT_DIR / lang / country_slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def _build_travel_assist_card(content_type, city_name, lang, country_slug):
    """Generate Travel Assistance Card HTML based on article content type.
    Uses affiliate links from config/affiliates.py."""
    from config.affiliates import hotels_link, flights_link, tours_link, insurance_link

    city_slug = city_name.lower().replace(" ", "-")

    # Get airport code for flights
    from config.destinations import DESTINATIONS
    destination_code = "MOW"
    country = DESTINATIONS.get(country_slug, {})
    for c_slug, city_data in country.get("cities", {}).items():
        if city_data.get("name_en", "").lower() == city_name.lower():
            codes = city_data.get("airport_codes", [])
            if codes:
                destination_code = codes[0]
            break

    if lang == "ru":
        title = "Помощь с планированием поездки"
        desc = "Если вы планируете поездку в этот регион, вы можете самостоятельно сравнить предложения у проверенных сервисов или оставить заявку на индивидуальный подбор тура."
        btn_tour = "Подобрать тур"
        btn_compare = "Сравнить предложения"
        note = "Ссылки ведут на проверенные сервисы с актуальными ценами."
    else:
        title = "Help planning your trip"
        desc = "If you're planning a trip to this region, you can compare offers from trusted services or leave a request for personalized tour selection."
        btn_tour = "Plan a trip"
        btn_compare = "Compare offers"
        note = "Links lead to trusted services with current prices."

    # Choose relevant services based on content type
    buttons = []

    if content_type in ("guide", "hotels"):
        buttons.append(("🏨 " + ("Забронировать отель" if lang == "ru" else "Book a hotel"),
                        hotels_link(city_slug)))
        buttons.append(("✈ " + ("Найти авиабилеты" if lang == "ru" else "Find flights"),
                        flights_link(destination=destination_code)))
        buttons.append(("🚕 " + ("Заказать трансфер" if lang == "ru" else "Book transfer"),
                        "https://tp.media/click?shmarker=736226&promo_id=3782&source_type=link&type=click&campaign_id=112&trs=kiwitaxi"))
        buttons.append(("📱 " + ("Купить eSIM" if lang == "ru" else "Get eSIM"),
                        "https://tp.media/click?shmarker=736226&promo_id=3803&source_type=link&type=click&campaign_id=118&trs=airalo"))

    elif content_type == "flights":
        buttons.append(("✈ " + ("Найти авиабилеты" if lang == "ru" else "Find flights"),
                        flights_link(destination=destination_code)))
        buttons.append(("🏨 " + ("Забронировать отель" if lang == "ru" else "Book a hotel"),
                        hotels_link(city_slug)))
        buttons.append(("🚌 " + ("Сравнить рейсы" if lang == "ru" else "Compare routes"),
                        "https://tp.media/click?shmarker=736226&promo_id=3799&source_type=link&type=click&campaign_id=114&trs=kiwicom"))

    elif content_type == "attractions":
        buttons.append(("🎟 " + ("Забронировать экскурсии" if lang == "ru" else "Book excursions"),
                        "https://tp.media/click?shmarker=736226&promo_id=3798&source_type=link&type=click&campaign_id=115&trs=getyourguide"))
        buttons.append(("🏨 " + ("Забронировать отель" if lang == "ru" else "Book a hotel"),
                        hotels_link(city_slug)))
        buttons.append(("🚕 " + ("Заказать трансфер" if lang == "ru" else "Book transfer"),
                        "https://tp.media/click?shmarker=736226&promo_id=3782&source_type=link&type=click&campaign_id=112&trs=kiwitaxi"))

    elif content_type == "seasons":
        buttons.append(("🏨 " + ("Забронировать отель" if lang == "ru" else "Book a hotel"),
                        hotels_link(city_slug)))
        buttons.append(("✈ " + ("Найти авиабилеты" if lang == "ru" else "Find flights"),
                        flights_link(destination=destination_code)))
        buttons.append(("🗺 " + ("Подобрать тур" if lang == "ru" else "Find a tour"),
                        tours_link(city_name)))

    # Always add tour request button
    buttons.append(("🎯 " + btn_tour, "#agent-form"))

    # Build HTML
    actions_html = ""
    for label, url in buttons:
        if url.startswith("#"):
            actions_html += f'<a href="{url}" class="travel-assist-btn travel-assist-btn-primary">{label}</a>\n'
        else:
            actions_html += f'<a href="{url}" target="_blank" rel="nofollow sponsored" class="travel-assist-btn travel-assist-btn-outline">{label}</a>\n'

    card_html = f'''<div class="travel-assist">
    <div class="travel-assist-header">
        <div class="travel-assist-icon">✈️</div>
        <div class="travel-assist-title">{title}</div>
    </div>
    <p class="travel-assist-desc">{desc}</p>
    <div class="travel-assist-actions">
        {actions_html}
    </div>
    <p class="travel-assist-note">{note}</p>
</div>'''

    return card_html


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
    body = inject_china_entry_info(body, country_slug, lang)

    import re as _re
    body = _re.sub(r'<h1[^>]*>.*?</h1>\s*', '', body, count=1)

    article_meta = {
        "title": article_data.get("title", ""),
        "meta_description": article_data.get("meta_description", ""),
        "h1": article_data.get("h1", ""),
        "body": body,
    }

    seo = build_seo_meta(article_meta, city_slug, country_slug, content_type, lang)

    # Country-specific OG image
    _og_map = {
        "russia": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1200&q=80",
        "baikal": "https://images.unsplash.com/photo-1551843073-4a9a5b6fcd5f?w=1200&q=80",
        "altai": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
        "karelia": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1200&q=80",
        "dagestan": "https://images.unsplash.com/photo-1568702846914-96b305d2ead1?w=1200&q=80",
        "kamchatka": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
        "mineral-vody": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1200&q=80",
        "vladivostok": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=1200&q=80",
        "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80",
        "thailand": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1200&q=80",
        "egypt": "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=1200&q=80",
        "uae": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80",
        "indonesia": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=1200&q=80",
        "china": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        "maldives": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1200&q=80",
        "sri-lanka": "https://images.unsplash.com/photo-1586526399017-e6d8cd50e1f7?w=1200&q=80",
        "montenegro": "https://images.unsplash.com/photo-1555990793-da11153b2473?w=1200&q=80",
        "vietnam": "https://images.unsplash.com/photo-1528127269322-539801943592?w=1200&q=80",
        "georgia": "https://images.unsplash.com/photo-1565008576549-57569a49371d?w=1200&q=80",
        "cyprus": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1200&q=80",
        "oman": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?w=1200&q=80",
    }
    seo["og_image"] = _og_map.get(country_slug, f"{os.getenv('SITE_URL', 'https://antondrakon.github.io/travel-content-site')}/assets/countries/travel-hero.webp")

    faq_data = generate_faq(city_name, content_type, lang, country_slug=country_slug, city_slug=city_slug)

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

    # Add hotel-specific structured data for AI search engines
    if content_type == "hotels":
        from agents.image_injector import find_hotel
        hotels_schema = []
        hotel_count = 0
        for line in body.split("\n"):
            import re as _re
            m = _re.search(r'<h3[^>]*>\s*(?:\d+\.\s*)?(?P<name>[A-ZА-Я][A-Za-zА-Яа-я\s&\-\'\.]{4,80}?)\s*(?:\([^)]*\))?\s*</h3>', line, _re.IGNORECASE)
            if m:
                hotel_name = m.group("name").strip()
                hotel = find_hotel(country_slug, city_slug, hotel_name)
                if hotel:
                    images = hotel.get("images", [])[:3]
                    schema_hotel = {
                        "@context": "https://schema.org",
                        "@type": "LodgingBusiness",
                        "name": hotel_name,
                        "address": {
                            "@type": "PostalAddress",
                            "addressLocality": city_name,
                            "addressCountry": country_name,
                        },
                        "image": [f"https://antondrakon.github.io{img['src']}" for img in images if img.get("src")],
                        "description": hotel.get("description", ""),
                        "priceRange": hotel.get("price", ""),
                        "telephone": "",
                    }
                    hotels_schema.append(schema_hotel)
                    hotel_count += 1
                    if hotel_count >= 10:
                        break
        if hotels_schema:
            schema_data.append({"@context": "https://schema.org", "@graph": hotels_schema})

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

    # Dynamic dates for article meta
    from datetime import date
    today = date.today()
    month_names_ru = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь",
    }
    month_names_en = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December",
    }
    month_ru = month_names_ru[today.month]
    month_en = month_names_en[today.month]
    date_iso = today.isoformat()
    date_display_ru = f"{month_ru} {today.year}"
    date_display_en = f"{month_en} {today.year}"

    # Generate Travel Assistance Card
    travel_assist = _build_travel_assist_card(content_type, city_name, lang, country_slug)

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
        og_image=seo.get("og_image", ""),
        date_published=date_iso,
        date_modified=date_iso,
        date_display_ru=date_display_ru,
        date_display_en=date_display_en,
        travel_assist=travel_assist,
    )

    out = OUTPUT_DIR / lang / country_slug / f"{content_type_slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_index_redirect():
    html = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta http-equiv="refresh" content="0;url=/en/index.html">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="/en/index.html">
<title>TravelHub</title><script>window.location.href="/en/index.html";</script></head>
<body><p>Redirecting to <a href="/en/index.html">TravelHub</a>...</p></body></html>"""
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")


def build_about_page(lang):
    template = env.get_template("about.html")
    html = template.render(lang=lang, breadcrumbs=[
        {"label": "Home" if lang == "en" else "Главная", "url": f"/{lang}/index.html"},
        {"label": "About" if lang == "en" else "О нас", "url": f"/{lang}/about.html"},
    ])
    out = OUTPUT_DIR / lang / "about.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_contacts_page(lang):
    template = env.get_template("contacts.html")
    html = template.render(lang=lang, breadcrumbs=[
        {"label": "Home" if lang == "en" else "Главная", "url": f"/{lang}/index.html"},
        {"label": "Contacts" if lang == "en" else "Контакты", "url": f"/{lang}/contacts.html"},
    ])
    out = OUTPUT_DIR / lang / "contacts.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_all():
    print("\n=== Building site ===\n")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build Tailwind CSS
    print("Building Tailwind CSS...")
    try:
        import subprocess
        result = subprocess.run(
            ["npm", "run", "tailwind:build"],
            cwd=str(Path(__file__).parent),
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("  Tailwind CSS built successfully")
        else:
            print(f"  Warning: Tailwind build failed: {result.stderr}")
    except Exception as e:
        print(f"  Warning: Could not build Tailwind CSS: {e}")
        print("  Using existing CSS file")

    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    for lang in ["ru", "en"]:
        print(f"\n[{lang.upper()}] Building home page...")
        build_home_page(lang)
        print(f"\n[{lang.upper()}] Building about page...")
        build_about_page(lang)
        print(f"\n[{lang.upper()}] Building contacts page...")
        build_contacts_page(lang)

    for country_slug in DESTINATIONS:
        for lang in ["ru", "en"]:
            print(f"\n[{lang.upper()}] Building {country_slug}...")
            build_destination_page(country_slug, lang)
            for city_slug in DESTINATIONS[country_slug]["cities"]:
                for ct_slug in CONTENT_TYPES:
                    build_article_page(country_slug, city_slug, ct_slug, lang)

    build_index_redirect()
    
    # Minify HTML files
    print("\nMinifying HTML files...")
    try:
        from minify_html import minify_directory
        results = minify_directory(OUTPUT_DIR, ['.html'])
        total_original = sum(r.get('original_size', 0) for r in results)
        total_minified = sum(r.get('minified_size', 0) for r in results)
        reduction = round((1 - total_minified / total_original) * 100, 1) if total_original > 0 else 0
        print(f"  Minified {len(results)} files: {total_original:,} → {total_minified:,} bytes ({reduction}% reduction)")
    except Exception as e:
        print(f"  Warning: HTML minification failed: {e}")
    
    print("\n=== Site built ===\n")


if __name__ == "__main__":
    build_all()
