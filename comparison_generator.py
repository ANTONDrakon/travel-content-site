"""
Comparison Pages Generator for TravelHub
Generates "Turkey vs Egypt", "Thailand vs Vietnam" etc. comparison pages.
"""
import os
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path(__file__).parent / "docs"
SITE_URL = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")

# Comparison data for popular destination pairs
COMPARISONS = {
    "turkey-vs-egypt": {
        "dest1": "turkey",
        "dest2": "egypt",
        "hero_image": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1600&q=80",
        "ru": {
            "title": "Турция vs Египет: что выбрать в 2026?",
            "subtitle": "Подробное сравнение двух популярных направлений для отдыха",
            "meta_description": "Турция или Египет? Сравниваем погоду, цены, отели, пляжи, экскурсии. Подробный гид для выбора направления.",
            "comparison_rows": [
                {"label": "Погода летом", "value1": "+28-38°C", "value2": "+30-40°C"},
                {"label": "Погода зимой", "value1": "+5-16°C", "value2": "+22-28°C"},
                {"label": "Виза", "value1": "Безвиз 90 дней", "value2": "По прибытии $25"},
                {"label": "Средний бюджет/неделю", "value1": "от ₽70 000", "value2": "от ₽60 000"},
                {"label": "All Inclusive", "value1": "от ₽4 000/ночь", "value2": "от ₽3 500/ночь"},
                {"label": "Море", "value1": "Средиземное + Эгейское", "value2": "Красное море"},
                {"label": "Дайвинг", "value1": "Хороший", "value2": "Один из лучших в мире"},
                {"label": "Экскурсии", "value1": "Исторические (Эфес, Каппадокия)", "value2": "Древние (пирамиды, Луксор)"},
                {"label": "Кухня", "value1": "Турецкая (кебабы, мезе)", "value2": "Египетская (фалафель, кушари)"},
                {"label": "Безопасность", "value1": "Высокая", "value2": "Высокая на курортах"},
            ],
            "dest1_advantages": [
                "Безвизовый въезд до 90 дней",
                "Разнообразные курорты (пляжи, горы, города)",
                "Европейская инфраструктура",
                "Богатая история и культура",
                "Отличная кухня",
                "Развитый шопинг",
            ],
            "dest2_advantages": [
                "Один из лучших дайвингов в мире",
                "Круглогодичное тепло",
                "Древнейшая цивилизация (пирамиды)",
                "Более бюджетный отдых",
                "All Inclusive отели",
                "Тёплое море даже зимой",
            ],
            "verdict": """
<h3>Когда выбирать Турцию?</h3>
<p>Турция — универсальное направление. Идеально для семейного отдыха, экскурсий, шопинга. Безвизовый въезд, разнообразные курорты, европейский уровень сервиса.</p>

<h3>Когда выбирать Египет?</h3>
<p>Египет — лучший выбор для дайвинга и бюджетного отдыха. Красное море — один из лучших подводных миров. Пирамиды и Луксор — уникальные экскурсии.</p>

<h3>Наш вывод</h3>
<p>Оба направления отличные. Турция — для тех, кто хочет разнообразие и комфорт. Египет — для дайверов и любителей древней истории. Оба доступны по цене и не требуют визы (или виза по прибытии).</p>
""",
        },
        "en": {
            "title": "Turkey vs Egypt: Which to Choose in 2026?",
            "subtitle": "Detailed comparison of two popular vacation destinations",
            "meta_description": "Turkey or Egypt? Compare weather, prices, hotels, beaches, excursions. Detailed guide for choosing a destination.",
            "comparison_rows": [
                {"label": "Summer weather", "value1": "+28-38°C", "value2": "+30-40°C"},
                {"label": "Winter weather", "value1": "+5-16°C", "value2": "+22-28°C"},
                {"label": "Visa", "value1": "Visa-free 90 days", "value2": "On arrival $25"},
                {"label": "Avg budget/week", "value1": "from $700", "value2": "from $600"},
                {"label": "All Inclusive", "value1": "from $40/night", "value2": "from $35/night"},
                {"label": "Sea", "value1": "Mediterranean + Aegean", "value2": "Red Sea"},
                {"label": "Diving", "value1": "Good", "value2": "World-class"},
                {"label": "Excursions", "value1": "Historical (Ephesus, Cappadocia)", "value2": "Ancient (pyramids, Luxor)"},
                {"label": "Cuisine", "value1": "Turkish (kebabs, meze)", "value2": "Egyptian (falafel, koshari)"},
                {"label": "Safety", "value1": "High", "value2": "High at resorts"},
            ],
            "dest1_advantages": [
                "Visa-free entry for 90 days",
                "Diverse resorts (beaches, mountains, cities)",
                "European infrastructure",
                "Rich history and culture",
                "Excellent cuisine",
                "Developed shopping",
            ],
            "dest2_advantages": [
                "World-class diving",
                "Year-round warmth",
                "Ancient civilization (pyramids)",
                "More budget-friendly",
                "All Inclusive hotels",
                "Warm sea even in winter",
            ],
            "verdict": """
<h3>When to choose Turkey?</h3>
<p>Turkey is a universal destination. Perfect for family vacations, sightseeing, and shopping. Visa-free entry, diverse resorts, European service level.</p>

<h3>When to choose Egypt?</h3>
<p>Egypt is the best choice for diving and budget travel. The Red Sea is one of the best underwater worlds. Pyramids and Luxor are unique excursions.</p>

<h3>Our verdict</h3>
<p>Both destinations are excellent. Turkey is for those who want variety and comfort. Egypt is for divers and lovers of ancient history. Both are affordable and don't require visas (or visa on arrival).</p>
""",
        },
    },
    "thailand-vs-vietnam": {
        "dest1": "thailand",
        "dest2": "vietnam",
        "hero_image": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1600&q=80",
        "ru": {
            "title": "Таиланд vs Вьетнам: что выбрать в 2026?",
            "subtitle": "Сравнение двух лучших направлений Юго-Восточной Азии",
            "meta_description": "Таиланд или Вьетнам? Сравниваем погоду, цены, пляжи, еду, визу. Подробный гид для выбора.",
            "comparison_rows": [
                {"label": "Виза", "value1": "Безвиз 60 дней", "value2": "Безвиз 45 дней"},
                {"label": "Средний бюджет/неделю", "value1": "от ₽90 000", "value2": "от ₽40 000"},
                {"label": "Питание в кафе", "value1": "от ₽200", "value2": "от ₽100"},
                {"label": "Массаж", "value1": "от ₽350", "value2": "от ₽200"},
                {"label": "Пляжи", "value1": "Пхукет, Самуи, Краби", "value2": "Фукуок, Нячанг, Дананг"},
                {"label": "Кухня", "value1": "Тайская (Пад Тай, Том Ям)", "value2": "Вьетнамская (Фо, Баньмы)"},
                {"label": "Дайвинг", "value1": "Симиланы, Ко Тао", "value2": "Фукуок, Нячанг"},
                {"label": "Ночная жизнь", "value1": "Паттайя, Бангкок", "value2": "Хо Ши Minh"},
                {"label": "Природа", "value1": "Храмы, джунгли", "value2": "Халонг-Бей, Сапа"},
                {"label": "Инфраструктура", "value1": "Развитая", "value2": "Развивающаяся"},
            ],
            "dest1_advantages": [
                "Более развитая туристическая инфраструктура",
                "Лучший дайвинг в регионе",
                "Богатая ночная жизнь",
                "Отличный сервис",
                "Много развлечений для семей",
                "Удобный транспорт",
            ],
            "dest2_advantages": [
                "В 2-3 раза дешевле Таиланда",
                "Более аутентичная Азия",
                "Уникальная кухня",
                "Живописная природа (Халонг-Бей)",
                "Меньше туристов",
                "Богатая история",
            ],
            "verdict": """
<h3>Когда выбирать Таиланд?</h3>
<p>Таиланд — для тех, кто хочет комфорт, развитую инфраструктуру и разнообразный отдых. Лучший дайвинг, ночная жизнь, сервис.</p>

<h3>Когда выбирать Вьетнам?</h3>
<p>Вьетнам — для тех, кто хочет аутентичную Азию и сэкономить. В 2-3 раза дешевле, уникальная кухня, живописная природа.</p>

<h3>Наш вывод</h3>
<p>Таиланд — комфорт и сервис. Вьетнам — аутентичность и бюджет. Оба направления отличные для первого опыта в Азии.</p>
""",
        },
        "en": {
            "title": "Thailand vs Vietnam: Which to Choose in 2026?",
            "subtitle": "Comparison of two best Southeast Asian destinations",
            "meta_description": "Thailand or Vietnam? Compare weather, prices, beaches, food, visa. Detailed guide for choosing.",
            "comparison_rows": [
                {"label": "Visa", "value1": "Visa-free 60 days", "value2": "Visa-free 45 days"},
                {"label": "Avg budget/week", "value1": "from $900", "value2": "from $400"},
                {"label": "Meal at cafe", "value1": "from $2", "value2": "from $1"},
                {"label": "Massage", "value1": "from $3.50", "value2": "from $2"},
                {"label": "Beaches", "value1": "Phuket, Samui, Krabi", "value2": "Phu Quoc, Nha Trang, Da Nang"},
                {"label": "Cuisine", "value1": "Thai (Pad Thai, Tom Yum)", "value2": "Vietnamese (Pho, Banh Mi)"},
                {"label": "Diving", "value1": "Similans, Koh Tao", "value2": "Phu Quoc, Nha Trang"},
                {"label": "Nightlife", "value1": "Pattaya, Bangkok", "value2": "Ho Chi Minh"},
                {"label": "Nature", "value1": "Temples, jungles", "value2": "Ha Long Bay, Sapa"},
                {"label": "Infrastructure", "value1": "Developed", "value2": "Developing"},
            ],
            "dest1_advantages": [
                "More developed tourist infrastructure",
                "Best diving in the region",
                "Vibrant nightlife",
                "Excellent service",
                "Many family attractions",
                "Convenient transport",
            ],
            "dest2_advantages": [
                "2-3x cheaper than Thailand",
                "More authentic Asia",
                "Unique cuisine",
                "Scenic nature (Ha Long Bay)",
                "Fewer tourists",
                "Rich history",
            ],
            "verdict": """
<h3>When to choose Thailand?</h3>
<p>Thailand is for those who want comfort, developed infrastructure, and diverse recreation. Best diving, nightlife, service.</p>

<h3>When to choose Vietnam?</h3>
<p>Vietnam is for those who want authentic Asia and savings. 2-3x cheaper, unique cuisine, scenic nature.</p>

<h3>Our verdict</h3>
<p>Thailand = comfort and service. Vietnam = authenticity and budget. Both are excellent for a first experience in Asia.</p>
""",
        },
    },
    "maldives-vs-sri-lanka": {
        "dest1": "maldives",
        "dest2": "sri-lanka",
        "hero_image": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1600&q=80",
        "ru": {
            "title": "Мальдивы vs Шри-Ланка: что выбрать в 2026?",
            "subtitle": "Два островных направления — два стиля отдыха",
            "meta_description": "Мальдивы или Шри-Ланка? Сравниваем цены, пляжи, визу, природу. Что выбрать?",
            "comparison_rows": [
                {"label": "Виза", "value1": "Бесплатно 30 дней", "value2": "ETA $50"},
                {"label": "Средний бюджет/неделю", "value1": "от ₽250 000", "value2": "от ₽50 000"},
                {"label": "Питание", "value1": "На курорте ($20-50)", "value2": "Местное ($2-5)"},
                {"label": "Пляжи", "value1": "Белый песок, бирюза", "value2": "Золотой песок, океан"},
                {"label": "Дайвинг", "value1": "Лучший в мире", "value2": "Хороший"},
                {"label": "Природа", "value1": "Коралловые рифы", "value2": "Джунгли, горы, водопады"},
                {"label": "Экскурсии", "value1": "Минимум", "value2": "Храмы, сафари, плантации"},
                {"label": "Отдых", "value1": "Пляж, спа, дайвинг", "value2": "Пляжи + экскурсии + природа"},
            ],
            "dest1_advantages": [
                "Лучший дайвинг в мире",
                "Бирюзовые лагуны",
                "Водные виллы",
                "Полный релакс",
                "Романтический отдых",
                "Бесплатная виза",
            ],
            "dest2_advantages": [
                "В 5 раз дешевле Мальдив",
                "Разнообразная природа",
                "Храмы и культура",
                "Сафари",
                "Чайные плантации",
                "Активный отдых",
            ],
            "verdict": """
<h3>Когда выбирать Мальдивы?</h3>
<p>Мальдивы — для тех, кто хочет абсолютный релакс, дайвинг и романтику. Бюджет от ₽250 000 на человека.</p>

<h3>Когда выбирать Шри-Ланку?</h3>
<p>Шри-Ланка — для тех, кто хочет разнообразный отдых: пляжи + экскурсии + природа + культура. Бюджет от ₽50 000.</p>

<h3>Наш вывод</h3>
<p>Мальдивы = релакс и дайвинг. Шри-Ланка = разнообразие и бюджет. Выбор зависит от бюджета и целей поездки.</p>
""",
        },
        "en": {
            "title": "Maldives vs Sri Lanka: Which to Choose in 2026?",
            "subtitle": "Two island destinations — two vacation styles",
            "meta_description": "Maldives or Sri Lanka? Compare prices, beaches, visa, nature. What to choose?",
            "comparison_rows": [
                {"label": "Visa", "value1": "Free 30 days", "value2": "ETA $50"},
                {"label": "Avg budget/week", "value1": "from $2,500", "value2": "from $500"},
                {"label": "Food", "value1": "At resort ($20-50)", "value2": "Local ($2-5)"},
                {"label": "Beaches", "value1": "White sand, turquoise", "value2": "Golden sand, ocean"},
                {"label": "Diving", "value1": "World's best", "value2": "Good"},
                {"label": "Nature", "value1": "Coral reefs", "value2": "Jungles, mountains, waterfalls"},
                {"label": "Excursions", "value1": "Minimal", "value2": "Temples, safari, plantations"},
                {"label": "Vacation type", "value1": "Beach, spa, diving", "value2": "Beaches + excursions + nature"},
            ],
            "dest1_advantages": [
                "World's best diving",
                "Turquoise lagoons",
                "Overwater villas",
                "Complete relaxation",
                "Romantic vacation",
                "Free visa",
            ],
            "dest2_advantages": [
                "5x cheaper than Maldives",
                "Diverse nature",
                "Temples and culture",
                "Safari",
                "Tea plantations",
                "Active vacation",
            ],
            "verdict": """
<h3>When to choose Maldives?</h3>
<p>Maldives is for absolute relaxation, diving, and romance. Budget from $2,500 per person.</p>

<h3>When to choose Sri Lanka?</h3>
<p>Sri Lanka is for diverse recreation: beaches + excursions + nature + culture. Budget from $500.</p>

<h3>Our verdict</h3>
<p>Maldives = relaxation and diving. Sri Lanka = variety and budget. Choice depends on budget and trip goals.</p>
""",
        },
    },
}


def build_comparison_page(slug, lang):
    """Build a comparison page."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    from publisher import get_country_image, DESTINATIONS_LIST
    from config.destinations import DESTINATIONS

    SITE_DIR = Path(__file__).parent / "site"
    TEMPLATES_DIR = SITE_DIR / "templates"

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    env.globals["site_url"] = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")
    from urllib.parse import urlparse as _urlparse
    _env_root = _urlparse(os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")).path.rstrip("/")
    env.globals["root"] = _env_root
    env.globals["formspree_id"] = "xnjyjnnd"
    env.globals["enumerate"] = enumerate

    # Analytics
    env.globals["analytics_enabled"] = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
    env.globals["yandex_metrika_id"] = os.getenv("YANDEX_METRIKA_ID", None)
    env.globals["google_analytics_id"] = os.getenv("GOOGLE_ANALYTICS_ID", None)
    env.globals["recaptcha_site_key"] = os.getenv("RECAPTCHA_SITE_KEY", None)

    from datetime import date
    env.globals["current_year"] = str(date.today().year)

    env.globals["destinations_list"] = DESTINATIONS_LIST
    env.globals["russia_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "russia"]
    env.globals["international_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "international"]

    comp = COMPARISONS[slug]
    data = comp[lang]

    dest1_country = DESTINATIONS.get(comp["dest1"], {})
    dest2_country = DESTINATIONS.get(comp["dest2"], {})

    emojis = {
        "turkey": "🇹🇷", "thailand": "🇹🇭", "egypt": "🇪🇬",
        "uae": "🇦🇪", "indonesia": "🇮🇩", "china": "🇨🇳", "maldives": "🇲🇻",
        "sri-lanka": "🇱🇰", "montenegro": "🇲🇪", "vietnam": "🇻🇳",
        "georgia": "🇬🇪", "cyprus": "🇨🇾", "oman": "🇴🇲",
    }

    dest1 = {
        "slug": comp["dest1"],
        "name_ru": dest1_country.get("name_ru", comp["dest1"]),
        "name_en": dest1_country.get("name_en", comp["dest1"].title()),
        "image": get_country_image(comp["dest1"]),
        "emoji": emojis.get(comp["dest1"], "🌍"),
        "advantages": data["dest1_advantages"],
    }

    dest2 = {
        "slug": comp["dest2"],
        "name_ru": dest2_country.get("name_ru", comp["dest2"]),
        "name_en": dest2_country.get("name_en", comp["dest2"].title()),
        "image": get_country_image(comp["dest2"]),
        "emoji": emojis.get(comp["dest2"], "🌍"),
        "advantages": data["dest2_advantages"],
    }

    template = env.get_template("comparison.html")
    html = template.render(
        lang=lang,
        slug=slug,
        title=data["title"],
        meta_description=data["meta_description"],
        subtitle=data["subtitle"],
        hero_image=comp["hero_image"],
        dest1=dest1,
        dest2=dest2,
        comparison_rows=data["comparison_rows"],
        verdict=data["verdict"],
        alternate_url=f"compare/{slug}.html",
    )

    out = OUTPUT_DIR / lang / "compare" / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_all_comparisons():
    """Build all comparison pages for all languages."""
    print("\n=== Building comparison pages ===\n")

    for slug in COMPARISONS:
        for lang in ["ru", "en"]:
            build_comparison_page(slug, lang)

    print("\n=== Comparison pages done ===\n")


if __name__ == "__main__":
    build_all_comparisons()
