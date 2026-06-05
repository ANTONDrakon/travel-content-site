import os
import json
import shutil
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

env.globals["site_url"] = os.getenv("SITE_URL", "https://YOUR_USERNAME.github.io/travel-content-site")
env.globals["enumerate"] = enumerate


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_articles_index():
    path = CONTENT_DIR / "articles_index.json"
    return load_json(path)


def get_country_emoji(slug):
    emojis = {
        "turkey": "🇹🇷", "thailand": "🇹🇭", "egypt": "🇪🇬",
        "uae": "🇦🇪", "indonesia": "🇮🇩",
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
            "cities": country["cities"],
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
    from agents.seo_optimizer import get_url_slug, SLUGS_RU, SLUGS_EN
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

    template = env.get_template("destination.html")
    html = template.render(
        lang=lang,
        country=country,
        cities=country["cities"],
        all_articles=all_articles,
        articles_count=len(country["cities"]) * 5,
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

    article_meta = {
        "title": article_data.get("title", ""),
        "meta_description": article_data.get("meta_description", ""),
        "h1": article_data.get("h1", ""),
        "body": article_data.get("body", ""),
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
                "title": city_name_for_breadcrumb if lang == "ru" else city_name_for_breadcrumb,
                "type": ct_info["category_ru"] if lang == "ru" else ct_info["category_en"],
            })

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
    )

    out = OUTPUT_DIR / lang / country_slug / f"{content_type_slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def build_index_redirect():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/en/index.html">
    <title>Travel Guide Hub</title>
    <script>window.location.href="/en/index.html";</script>
</head>
<body>
    <p>Redirecting to <a href="/en/index.html">Travel Guide Hub</a>...</p>
</body>
</html>"""
    out = OUTPUT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"  Built root redirect: {out}")


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
            print(f"\n[{lang.upper()}] Building {country_slug} destination...")
            build_destination_page(country_slug, lang)

            for city_slug in DESTINATIONS[country_slug]["cities"]:
                for ct_slug in CONTENT_TYPES:
                    build_article_page(country_slug, city_slug, ct_slug, lang)

    build_index_redirect()

    print("\n=== Site built successfully! ===\n")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print(f"Open: {OUTPUT_DIR / 'index.html'}")


if __name__ == "__main__":
    build_all()
