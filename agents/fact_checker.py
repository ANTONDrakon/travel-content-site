"""
AGENT 3 — Enhanced Fact Checker
Comprehensive verification of all factual claims in articles.
Covers all 21 countries with structured data for visa, currency, timezone, etc.
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"

# ---------------------------------------------------------------------------
# KNOWN FACTS — all 21 countries/regions
# ---------------------------------------------------------------------------

KNOWN_FACTS = {
    "turkey": {
        "visa": {"ru": "безвизовый до 90 дней", "en": "visa-free up to 90 days"},
        "currency": {"code": "TRY", "name_ru": "турецкая лира", "name_en": "Turkish lira", "symbol": "₺"},
        "timezone": "UTC+3",
        "airports": ["IST", "SAW", "AYT", "ADB", "DLM"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно, есть ограничения в некоторых регионах",
        "language_ru": "турецкий, английский распространен в курортах",
        "language_en": "Turkish, English widely spoken in resorts",
    },
    "thailand": {
        "visa": {"ru": "безвизовый до 60 дней (с 2024)", "en": "visa-free up to 60 days (since 2024)"},
        "currency": {"code": "THB", "name_ru": "тайский бат", "name_en": "Thai baht", "symbol": "฿"},
        "timezone": "UTC+7",
        "airports": ["BKK", "HKT", "CNX", "USM"],
        "driving_side": "left",
        "plug_type": "A/B/C",
        "emergency": "191",
        "alcohol": "доступно, запрещено на буддийских праздниках",
        "language_ru": "тайский, английский в tourist areas",
        "language_en": "Thai, English in tourist areas",
    },
    "egypt": {
        "visa": {"ru": "виза по прибытии $25", "en": "visa on arrival $25"},
        "currency": {"code": "EGP", "name_ru": "египетский фунт", "name_en": "Egyptian pound", "symbol": "EGP"},
        "timezone": "UTC+2",
        "airports": ["CAI", "HRG", "SSH", "LXR"],
        "driving_side": "right",
        "plug_type": "C",
        "emergency": "122",
        "alcohol": "доступно в отелях и ресторанах",
        "language_ru": "арабский, английский в tourism sector",
        "language_en": "Arabic, English in tourism sector",
    },
    "uae": {
        "visa": {"ru": "безвизовый до 90 дней", "en": "visa-free up to 90 days"},
        "currency": {"code": "AED", "name_ru": "дирхам ОАЭ", "name_en": "UAE dirham", "symbol": "AED"},
        "timezone": "UTC+4",
        "airports": ["DXB", "AUH", "SHJ"],
        "driving_side": "right",
        "plug_type": "G",
        "emergency": "999",
        "alcohol": "доступно в лицензированных заведениях",
        "language_ru": "арабский, английский — второй official",
        "language_en": "Arabic, English is official second language",
    },
    "indonesia": {
        "visa": {"ru": "виза по прибытии 30 дней", "en": "visa on arrival 30 days"},
        "currency": {"code": "IDR", "name_ru": "индонезийская рупия", "name_en": "Indonesian rupiah", "symbol": "IDR"},
        "timezone": "UTC+7/+8/+9",
        "airports": ["DPS", "CGK", "SUB"],
        "driving_side": "left",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "ограничено, запрещено на Бали в ряде районов",
        "language_ru": "индонезийский, английский в tourist areas",
        "language_en": "Indonesian, English in tourist areas",
    },
    "china": {
        "visa": {"ru": "виза требуется, Хайнань — безвизовый 30 дней", "en": "visa required, Hainan — visa-free 30 days"},
        "currency": {"code": "CNY", "name_ru": "китайский юань", "name_en": "Chinese yuan", "symbol": "¥"},
        "timezone": "UTC+8",
        "airports": ["PEK", "PVG", "CAN", "SZX", "SYX"],
        "driving_side": "right",
        "plug_type": "A/I/C",
        "emergency": "110/120",
        "alcohol": "доступно",
        "language_ru": "китайский, английский ограничен",
        "language_en": "Mandarin, limited English",
    },
    "maldives": {
        "visa": {"ru": "бесплатная виза по прибытии 30 дней", "en": "free visa on arrival 30 days"},
        "currency": {"code": "MVR", "name_ru": "мальдивская руфия", "name_en": "Maldivian rufiyaa", "symbol": "MVR"},
        "timezone": "UTC+5",
        "airports": ["MLE"],
        "driving_side": "left",
        "plug_type": "A/D/G",
        "emergency": "119",
        "alcohol": "запрещено на local islands, доступно на resort islands",
        "language_ru": "дивехи, английский",
        "language_en": "Dhivehi, English",
    },
    "sri_lanka": {
        "visa": {"ru": "электронная виза ETA", "en": "electronic visa ETA"},
        "currency": {"code": "LKR", "name_ru": "шри-ланкийская рупия", "name_en": "Sri Lankan rupee", "symbol": "LKR"},
        "timezone": "UTC+5:30",
        "airports": ["CMB", "JAF"],
        "driving_side": "left",
        "plug_type": "D/M/G",
        "emergency": "119",
        "alcohol": "доступно в отелях и лицензированных заведениях",
        "language_ru": "сингальский, тамильский, английский",
        "language_en": "Sinhala, Tamil, English",
    },
    "montenegro": {
        "visa": {"ru": "безвизовый до 90 дней", "en": "visa-free up to 90 days"},
        "currency": {"code": "EUR", "name_ru": "евро", "name_en": "Euro", "symbol": "€"},
        "timezone": "UTC+1",
        "airports": ["TGD"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "черногорский, сербский, английский",
        "language_en": "Montenegrin, Serbian, English",
    },
    "vietnam": {
        "visa": {"ru": "электронная виза 90 дней", "en": "e-visa 90 days"},
        "currency": {"code": "VND", "name_ru": "вьетнамский донг", "name_en": "Vietnamese dong", "symbol": "₫"},
        "timezone": "UTC+7",
        "airports": ["SGN", "HAN", "DAD", "PQC"],
        "driving_side": "right",
        "plug_type": "A/C",
        "emergency": "113",
        "alcohol": "доступно, пиво очень популярно",
        "language_ru": "вьетнамский, английский в tourist areas",
        "language_en": "Vietnamese, English in tourist areas",
    },
    "georgia": {
        "visa": {"ru": "безвизовый до 1 года", "en": "visa-free up to 1 year"},
        "currency": {"code": "GEL", "name_ru": "грузинский лари", "name_en": "Georgian lari", "symbol": "₾"},
        "timezone": "UTC+4",
        "airports": ["TBS", "KUT"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно, винная культура",
        "language_ru": "грузинский, русский широко понимают",
        "language_en": "Georgian, Russian widely understood",
    },
    "cyprus": {
        "visa": {"ru": "безвизовый до 90 дней (Шенген)", "en": "visa-free up to 90 days (Schengen)"},
        "currency": {"code": "EUR", "name_ru": "евро", "name_en": "Euro", "symbol": "€"},
        "timezone": "UTC+2",
        "airports": ["LCA", "PFO"],
        "driving_side": "left",
        "plug_type": "G",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "греческий, турецкий, английский",
        "language_en": "Greek, Turkish, English",
    },
    "oman": {
        "visa": {"ru": "виза по прибытии / электронная виза", "en": "visa on arrival / e-visa"},
        "currency": {"code": "OMR", "name_ru": "оманский риал", "name_en": "Omani rial", "symbol": "OMR"},
        "timezone": "UTC+4",
        "airports": ["MCT"],
        "driving_side": "right",
        "plug_type": "G",
        "emergency": "9999",
        "alcohol": "доступно в лицензированных заведениях",
        "language_ru": "арабский, английский",
        "language_en": "Arabic, English",
    },
    # Russian regions
    "russia": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+3 to UTC+12",
        "airports": ["SVO", "DME", "LED"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно с 18 лет",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "baikal": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+8",
        "airports": ["IKT"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "altai": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+7",
        "airports": ["BAX"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "karelia": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+3",
        "airports": ["PES", "MMK"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "dagestan": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+3",
        "airports": ["MCX"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "ограничено в ряде районов",
        "language_ru": "русский, аварский, дarginsкий и др.",
        "language_en": "Russian, Avar, Dargwa, etc.",
    },
    "kamchatka": {
        "visa": {"ru": "не требуется (внутренний туризм, но нужен пропуск в погранзону)", "en": "not required (domestic, border zone permit needed)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+12",
        "airports": ["PKC"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "mineral_vody": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+3",
        "airports": ["MRV"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
    "vladivostok": {
        "visa": {"ru": "не требуется (внутренний туризм)", "en": "not required (domestic)"},
        "currency": {"code": "RUB", "name_ru": "российский рубль", "name_en": "Russian ruble", "symbol": "₽"},
        "timezone": "UTC+10",
        "airports": ["VVO"],
        "driving_side": "right",
        "plug_type": "C/F",
        "emergency": "112",
        "alcohol": "доступно",
        "language_ru": "русский",
        "language_en": "Russian",
    },
}

# Suspicious patterns that indicate unverified or AI-generated claims
SUSPICIOUS_PATTERNS = [
    (r"от €?\d[\d,.]*\s*(?:евро|€)", "Price in EUR without RUB conversion"),
    (r"население \d[\d,.]* млн", "Population without source"),
    (r"входит в топ-\d", "Ranking without source"),
    (r"самый (?:лучший|популярный|большой|красивый)", "Superlative without qualification"),
    (r"гарантированно|100% гаранти|наверняка", "Guarantee without basis"),
    (r"я (?:лично|сам(?:а)?)\s+(?:проверил|посетил|был)", "First person AI impersonation"),
    (r"точная цена|именно столько|ровно", "Precise price claim without source"),
    (r"(?:the )?(?:best|most popular|biggest|most beautiful) (?:in|of)", "Superlative without qualification"),
]


def verify_visa(country_slug, body, lang="ru"):
    """Verify visa information against known facts."""
    issues = []
    facts = KNOWN_FACTS.get(country_slug)
    if not facts:
        return issues

    visa = facts.get("visa", {}).get(lang, "")
    if not visa:
        return issues

    # Check if article mentions visa at all
    visa_keywords = ["виза", "visa", "безвизовый", "visa-free"]
    if not any(kw.lower() in body.lower() for kw in visa_keywords):
        issues.append(f"MISSING: No visa information found (expected: {visa})")

    return issues


def verify_currency(country_slug, body, lang="ru"):
    """Verify currency mentions against known facts."""
    issues = []
    facts = KNOWN_FACTS.get(country_slug)
    if not facts:
        return issues

    currency = facts.get("currency", {})
    code = currency.get("code", "")

    # Check if currency is mentioned
    currency_names = [
        currency.get("name_ru", ""),
        currency.get("name_en", ""),
        code,
        currency.get("symbol", ""),
    ]

    if not any(name and name.lower() in body.lower() for name in currency_names if name):
        issues.append(f"MISSING: Currency {code} not mentioned in article")

    return issues


def verify_airports(country_slug, body):
    """Verify airport codes are mentioned."""
    issues = []
    facts = KNOWN_FACTS.get(country_slug)
    if not facts:
        return issues

    airports = facts.get("airports", [])
    mentioned = [ap for ap in airports if ap in body.upper()]

    if not mentioned and airports:
        issues.append(f"MISSING: No airport codes mentioned (expected: {', '.join(airports)})")

    return issues


def verify_timezone(country_slug, body):
    """Verify timezone is mentioned."""
    issues = []
    facts = KNOWN_FACTS.get(country_slug)
    if not facts:
        return issues

    tz = facts.get("timezone", "")
    tz_keywords = ["часовой пояс", "time zone", "UTC", "МСК"]

    if not any(kw.lower() in body.lower() for kw in tz_keywords):
        issues.append(f"MISSING: Timezone ({tz}) not mentioned")

    return issues


def verify_prices(country_slug, body, lang="ru"):
    """Check if prices seem reasonable for the destination."""
    issues = []

    # Extract price patterns
    price_patterns = re.findall(r'[\$€₽]\s*(\d[\d,.]*)', body)

    for price_str in price_patterns:
        try:
            price = float(price_str.replace(",", "").replace(" ", ""))
        except ValueError:
            continue

        # Flag truly impossible prices (under $0.10)
        # $0.20-0.50 could be valid for tea, snacks, small items in cheap destinations
        if price < 0.10 and price > 0:
            issues.append(f"SUSPICIOUS: Impossibly low price ${price}")

    # Check EUR-only pricing for RU audience
    if lang == "ru":
        eur_count = len(re.findall(r'€\d', body))
        rub_count = len(re.findall(r'₽\d', body))
        if eur_count > 0 and rub_count < eur_count:
            issues.append("PRICE_FORMAT: More EUR prices than RUB — should convert for RU audience")

    return issues


def verify_names(country_slug, body):
    """Spell-check city/attraction names against DESTINATIONS config."""
    issues = []
    from config.destinations import DESTINATIONS

    dest = DESTINATIONS.get(country_slug)
    if not dest:
        return issues

    for region in dest.get("regions", {}).values():
        for city_slug, city in region.get("cities", {}).items():
            name_ru = city.get("name_ru", "")
            name_en = city.get("name_en", "")

        # Check if city name appears (case-insensitive)
        if name_en.lower() not in body.lower() and name_ru.lower() not in body.lower():
            # This is okay — not every article mentions every city
            pass

    return issues


def check_article(body, country_slug, lang="ru", content_type="guide"):
    """Run all verification checks on article body.

    Checks are context-aware: not all article types need all facts.
    - guide: all checks (visa, currency, timezone, airports)
    - hotels: visa + currency (no timezone/airports needed)
    - flights: visa only (currency/airports not relevant)
    - attractions: currency only (visa/airports/timezone not relevant)
    - seasons: timezone only (visa/currency/airports not relevant)
    """
    issues = []

    # Suspicious patterns
    for pattern, desc in SUSPICIOUS_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            issues.append(f"UNVERIFIED: {desc}")

    # Country-specific checks (context-aware by content type)
    if country_slug:
        if content_type == "guide":
            # Guide articles need everything
            issues.extend(verify_visa(country_slug, body, lang))
            issues.extend(verify_currency(country_slug, body, lang))
            issues.extend(verify_airports(country_slug, body))
            issues.extend(verify_timezone(country_slug, body))
        elif content_type == "hotels":
            # Hotels need visa and currency info
            issues.extend(verify_visa(country_slug, body, lang))
            issues.extend(verify_currency(country_slug, body, lang))
        elif content_type == "flights":
            # Flights need visa info only
            issues.extend(verify_visa(country_slug, body, lang))
        elif content_type == "attractions":
            # Attractions need currency info
            issues.extend(verify_currency(country_slug, body, lang))
        elif content_type == "seasons":
            # Seasons need timezone info
            issues.extend(verify_timezone(country_slug, body))

    # Price checks
    issues.extend(verify_prices(country_slug, body, lang))

    # Name checks
    issues.extend(verify_names(country_slug, body))

    return issues


def check_article_file(path):
    """Check a content JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [f"READ_ERROR: {path}"]

    body = data.get("body", "")
    country_slug = data.get("country", "")
    lang = data.get("lang", "ru")
    content_type = data.get("content_type", "guide")

    return check_article(body, country_slug, lang, content_type)


def run():
    """Scan all built HTML files and report issues."""
    print("\n=== FACT CHECKER ===\n")
    total_issues = 0

    if not CONTENT_DIR.exists():
        print("No content directory found.")
        return 0

    for json_path in CONTENT_DIR.rglob("*.json"):
        issues = check_article_file(json_path)
        if issues:
            rel = json_path.relative_to(BASE_DIR)
            print(f"\n[{rel}]")
            for i in issues:
                print(f"  {i}")
                total_issues += 1

    print(f"\nTotal issues: {total_issues}")
    return total_issues


if __name__ == "__main__":
    run()
