"""
RSS Feed Generator for TravelHub
Generates RSS 2.0 feed with all articles for subscribers and aggregators.
"""
import os
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path(__file__).parent / "docs"
SITE_URL = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")
TODAY = date.today().strftime("%Y-%m-%d")


def generate_rss(lang="en"):
    """Generate RSS 2.0 feed for a language."""
    from config.destinations import DESTINATIONS
    from agents.seo_optimizer import get_url_slug
    from config.prompts import CONTENT_TYPES

    items = []

    for country_slug, country in DESTINATIONS.items():
        for city_slug, city_data in country["cities"].items():
            for ct_slug, ct_info in CONTENT_TYPES.items():
                page_slug = get_url_slug(ct_slug, city_slug, lang)
                url = f"{SITE_URL}/{lang}/{country_slug}/{page_slug}.html"

                city_name = city_data["name_en"] if lang == "en" else city_data["name_ru"]
                country_name = country["name_en"] if lang == "en" else country["name_ru"]
                category = ct_info["category_en"] if lang == "en" else ct_info["category_ru"]

                title_templates = {
                    "guide": {"en": f"{city_name} Travel Guide 2026", "ru": f"Путеводитель по {city_name} 2026"},
                    "hotels": {"en": f"Best Hotels in {city_name} 2026", "ru": f"Лучшие отели {city_name} 2026"},
                    "flights": {"en": f"Cheap Flights to {city_name} 2026", "ru": f"Дешёвые билеты в {city_name} 2026"},
                    "attractions": {"en": f"Top Things to Do in {city_name} 2026", "ru": f"Топ мест {city_name} 2026"},
                    "seasons": {"en": f"Best Time to Visit {city_name} 2026", "ru": f"Когда ехать в {city_name} 2026"},
                }

                title = title_templates.get(ct_slug, {}).get(lang, f"{city_name} {category} 2026")
                description = f"{category}: {city_name}, {country_name}. {title}"

                items.append({
                    "title": title,
                    "link": url,
                    "description": description,
                    "pubDate": TODAY,
                    "category": category,
                    "guid": url,
                })

    # Build RSS XML
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    lines.append('<channel>')

    if lang == "ru":
        lines.append(f'  <title>TravelHub — Путеводители на русском</title>')
        lines.append(f'  <link>{SITE_URL}/ru/index.html</link>')
        lines.append(f'  <description>Экспертные путеводители по 50+ городам в 20 странах. Отели, билеты, достопримечательности.</description>')
        lines.append(f'  <language>ru</language>')
    else:
        lines.append(f'  <title>TravelHub — Travel Guides</title>')
        lines.append(f'  <link>{SITE_URL}/en/index.html</link>')
        lines.append(f'  <description>Expert travel guides for 50+ cities across 20 countries. Hotels, flights, attractions.</description>')
        lines.append(f'  <language>en</language>')

    lines.append(f'  <lastBuildDate>{TODAY}</lastBuildDate>')
    lines.append(f'  <atom:link href="{SITE_URL}/sitemap-{lang}.xml" rel="self" type="application/rss+xml"/>')

    for item in items:
        lines.append('  <item>')
        lines.append(f'    <title><![CDATA[{item["title"]}]]></title>')
        lines.append(f'    <link>{item["link"]}</link>')
        lines.append(f'    <description><![CDATA[{item["description"]}]]></description>')
        lines.append(f'    <pubDate>{item["pubDate"]}</pubDate>')
        lines.append(f'    <category>{item["category"]}</category>')
        lines.append(f'    <guid isPermaLink="true">{item["guid"]}</guid>')
        lines.append('  </item>')

    lines.append('</channel>')
    lines.append('</rss>')

    filename = f"feed-{lang}.xml"
    out = OUTPUT_DIR / filename
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  RSS feed {lang}: {out} ({len(items)} items)")
    return out


def build_all_feeds():
    """Generate RSS feeds for all languages."""
    print("\n=== Generating RSS feeds ===\n")
    generate_rss("ru")
    generate_rss("en")
    print("\n=== RSS feeds done ===\n")


if __name__ == "__main__":
    build_all_feeds()
