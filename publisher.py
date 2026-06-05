import os
import json
from pathlib import Path

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
    "turkey": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200&q=80",
    "thailand": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1200&q=80",
    "egypt": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80",
    "uae": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80",
    "indonesia": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1200&q=80",
    "china": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200&q=80",
    "maldives": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1200&q=80",
}

CITY_IMAGES = {
    "istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=80",
    "antalya": "https://images.unsplash.com/photo-1504680177321-2e6a3f4358e1?w=800&q=80",
    "alanya": "https://images.unsplash.com/photo-1597074866923-dc0589150358?w=800&q=80",
    "bodrum": "https://images.unsplash.com/photo-1504898770365-14faca6a7320?w=800&q=80",
    "cappadocia": "https://images.unsplash.com/photo-1611516491426-03025e6043c8?w=800&q=80",
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80",
    "phuket": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "pattaya": "https://images.unsplash.com/photo-1506665531195-3566af2b4dfa?w=800&q=80",
    "koh-samui": "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=800&q=80",
    "krabi": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800&q=80",
    "sharm-el-sheikh": "https://images.unsplash.com/photo-1539635278303-d4002c07eae2?w=800&q=80",
    "hurghada": "https://images.unsplash.com/photo-1539635278303-d4002c07eae2?w=800&q=80",
    "cairo": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    "luxor": "https://images.unsplash.com/photo-1560012057-4372e14b9fdb?w=800&q=80",
    "marsa-alam": "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "abu-dhabi": "https://images.unsplash.com/photo-1512632578888-7928c05b1d3b?w=800&q=80",
    "sharjah": "https://images.unsplash.com/photo-1572443492525-f46d5c22e5b9?w=800&q=80",
    "ras-al-khaimah": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "fujairah": "https://images.unsplash.com/photo-1582719350-3f9b1ff050ad?w=800&q=80",
    "ubud": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
    "kuta": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80",
    "seminyak": "https://images.unsplash.com/photo-1539367628448-4bc5c9d171c8?w=800&q=80",
    "canggu": "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?w=800&q=80",
    "nusa-dua": "https://images.unsplash.com/photo-1573790387438-4da905039392?w=800&q=80",
    "sanya": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
    "haikou": "https://images.unsplash.com/photo-1517697471339-4aa32003c11a?w=800&q=80",
    "beijing": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "shanghai": "https://images.unsplash.com/photo-1538428494232-9c0d8a3ab403?w=800&q=80",
    "xian": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800&q=80",
    "male": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800&q=80",
    "hulhumale": "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "maafushi": "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=800&q=80",
    "dhigurah": "https://images.unsplash.com/photo-1505881502356-5a2a8c4c4a3e?w=800&q=80",
    "thulusdhoo": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800&q=80",
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
        alternate_url=f"{lang}/index.html",
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

    if country_slug == "uae":
        template = env.get_template("destination-uae.html")
    else:
        template = env.get_template("destination.html")

    city_descriptions = {
        "dubai": "Город будущего: небоскрёбы, шопинг, развлечения. Самый популярный эмират.",
        "abu-dhabi": "Столица ОАЭ: культура, Лувр, мечеть шейха Зайда. Спокойный и респектабельный.",
        "sharjah": "Культурная столица: музеи, heritage-районы. Самый строгий, но бюджетный.",
        "fujairah": "Единственный эмират на Индийском океане. Дайвинг, снорклинг, горы Хаджар.",
        "ras-al-khaimah": "Природа и приключения: самая высокая гора ОАЭ, мангровые заросли, уединение.",
        "dubai_en": "City of the future: skyscrapers, shopping, entertainment. The most popular emirate.",
        "abu-dhabi_en": "Capital of UAE: culture, Louvre, Sheikh Zayed Mosque. Calm and respectable.",
        "sharjah_en": "Cultural capital: museums, heritage districts. Strictest but most affordable.",
        "fujairah_en": "Only emirate on the Indian Ocean. Diving, snorkeling, Hajar Mountains.",
        "ras-al-khaimah_en": "Nature & adventure: UAE's highest mountain, mangroves, total seclusion.",
    }

    for city_slug in cities_with_images:
        desc_key = f"{city_slug}_en" if lang == "en" else city_slug
        cities_with_images[city_slug]["desc"] = city_descriptions.get(desc_key, "")

    html = template.render(
        lang=lang,
        country=country,
        cities=cities_with_images,
        city_names=city_names_list,
        articles_count=len(country["cities"]) * 5,
        hero_image=get_country_image(country_slug),
        insurance_link=insurance_link(),
        alternate_url=f"{lang}/{country_slug}/index.html",
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

    article_meta = {
        "title": article_data.get("title", ""),
        "meta_description": article_data.get("meta_description", ""),
        "h1": article_data.get("h1", ""),
        "body": body,
    }

    seo = build_seo_meta(article_meta, city_name, country_slug, content_type, lang)

    faq_data = generate_faq(city_name, content_type, lang)

    alt_url = f"{country_slug}/{content_type_slug}.html"
    url = f"/{lang}/{country_slug}/{content_type_slug}.html"

    schema_article = generate_schema_article(seo, city_name, country_name, url, lang)
    schema_faq = generate_schema_faq(faq_data)
    schema_data = [schema_article, schema_faq]

    city_name_for_breadcrumb = city["name_ru"] if lang == "ru" else city["name_en"]

    breadcrumbs = [
        {"label": "Home" if lang == "en" else "Главная", "url": f"/{lang}/index.html"},
        {"label": country_name, "url": f"/{lang}/{country_slug}/index.html"},
        {"label": city_name_for_breadcrumb, "url": None},
    ]

    related = []
    for ct_slug, ct_info in CONTENT_TYPES.items():
        if ct_slug != content_type:
            rel_slug = get_url_slug(ct_slug, city_slug, lang)
            related.append({
                "url": f"{country_slug}/{rel_slug}.html",
                "title": city_name_for_breadcrumb,
                "type": ct_info["category_ru"] if lang == "ru" else ct_info["category_en"],
            })

    hero_image = None
    if content_type == "guide":
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
        en_alt_url=alt_url if lang == "en" else alt_url,
        ru_alt_url=alt_url if lang == "ru" else alt_url,
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
