import os
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path(__file__).parent / "docs"
SITE_URL = os.getenv("SITE_URL", "https://YOUR_USERNAME.github.io/travel-content-site")

TODAY = date.today().strftime("%Y-%m-%d")


def generate_sitemap():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    lines.append(f"  <sitemap><loc>{SITE_URL}/sitemap-ru.xml</loc><lastmod>{TODAY}</lastmod></sitemap>")
    lines.append(f"  <sitemap><loc>{SITE_URL}/sitemap-en.xml</loc><lastmod>{TODAY}</lastmod></sitemap>")
    lines.append("</sitemapindex>")

    out = OUTPUT_DIR / "sitemap.xml"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Sitemap index: {out}")


def generate_lang_sitemap(lang):
    from config.destinations import DESTINATIONS
    from agents.seo_optimizer import get_url_slug

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('  xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    priority_map = {
        "guide": "1.0",
        "hotels": "0.9",
        "flights": "0.9",
        "attractions": "0.8",
        "seasons": "0.7",
    }

    lines.append(f"  <url><loc>{SITE_URL}/{lang}/index.html</loc><priority>1.0</priority><lastmod>{TODAY}</lastmod></url>")

    for country_slug, country in DESTINATIONS.items():
        lines.append(f"  <url><loc>{SITE_URL}/{lang}/{country_slug}/index.html</loc><priority>0.9</priority><lastmod>{TODAY}</lastmod></url>")

        for city_slug in country["cities"]:
            for ct_slug in ["guide", "hotels", "flights", "attractions", "seasons"]:
                page_slug = get_url_slug(ct_slug, city_slug, lang)
                priority = priority_map.get(ct_slug, "0.6")
                lines.append(f"  <url><loc>{SITE_URL}/{lang}/{country_slug}/{page_slug}.html</loc><priority>{priority}</priority><lastmod>{TODAY}</lastmod></url>")

    lines.append("</urlset>")

    filename = f"sitemap-{lang}.xml"
    out = OUTPUT_DIR / filename
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Sitemap {lang}: {out}  ({len(lines) - 4} URLs)")


def generate_robots():
    template = OUTPUT_DIR / ".." / "site" / "assets" / "robots.txt"
    if not template.exists():
        return
    content = template.read_text(encoding="utf-8").replace("{{ site_url }}", SITE_URL)
    out = OUTPUT_DIR / "robots.txt"
    out.write_text(content, encoding="utf-8")
    print(f"  Robots.txt: {out}")


def build_all_sitemaps():
    print("\n=== Generating sitemaps ===\n")
    generate_sitemap()
    generate_lang_sitemap("ru")
    generate_lang_sitemap("en")
    generate_robots()
    print("\n=== Sitemaps done ===\n")


if __name__ == "__main__":
    build_all_sitemaps()
