"""
AGENT 1 — Project Analyzer
Scans project state, identifies content gaps, and recommends priorities.
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"


def analyze_coverage():
    """Compare DESTINATIONS config against existing content JSON files."""
    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    coverage = {}
    for country_slug, dest in DESTINATIONS.items():
        country_coverage = {
            "name_ru": dest["name_ru"],
            "name_en": dest["name_en"],
            "cities": {},
            "total_expected": 0,
            "total_generated": 0,
        }
        # Handle both old structure (cities) and new structure (regions -> cities)
        cities = dest.get("cities", {})
        if not cities:
            for region_data in dest.get("regions", {}).values():
                cities.update(region_data.get("cities", {}))

        for city_slug, city in cities.items():
            city_coverage = {}
            for ct_slug in CONTENT_TYPES:
                expected = 2  # ru + en
                generated = 0
                for lang in ["ru", "en"]:
                    content_slug = _get_content_slug(ct_slug, city_slug, lang)
                    path = CONTENT_DIR / lang / country_slug / f"{content_slug}.json"
                    if path.exists():
                        generated += 1
                city_coverage[ct_slug] = {
                    "expected": expected,
                    "generated": generated,
                    "complete": generated == expected,
                }
                country_coverage["total_expected"] += expected
                country_coverage["total_generated"] += generated
            country_coverage["cities"][city_slug] = {
                "name_ru": city["name_ru"],
                "name_en": city["name_en"],
                "types": city_coverage,
            }
        coverage[country_slug] = country_coverage
    return coverage


def analyze_staleness(max_age_days=30):
    """Check file modification dates. Flag articles older than max_age_days."""
    stale = []
    cutoff = datetime.now().timestamp() - (max_age_days * 86400)

    if not CONTENT_DIR.exists():
        return stale

    for json_path in CONTENT_DIR.rglob("*.json"):
        mtime = json_path.stat().st_mtime
        if mtime < cutoff:
            age_days = int((datetime.now().timestamp() - mtime) / 86400)
            stale.append({
                "path": str(json_path.relative_to(BASE_DIR)),
                "age_days": age_days,
                "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"),
            })
    return stale


def analyze_affiliate_coverage():
    """For each article, check how many affiliate categories are represented."""
    results = []

    if not CONTENT_DIR.exists():
        return results

    for json_path in CONTENT_DIR.rglob("*.json"):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        body = data.get("body", "")
        categories_found = []
        for cat in ["hotels", "flights", "tours", "excursions", "transfers",
                     "esim", "car_rental", "insurance", "tickets"]:
            placeholders = [f"{{{cat}_placeholder}}", cat]
            if any(p in body for p in placeholders) or f"partner-link" in body:
                categories_found.append(cat)

        results.append({
            "path": str(json_path.relative_to(BASE_DIR)),
            "affiliate_categories": categories_found,
            "count": len(categories_found),
        })

    return results


def analyze_internal_links():
    """Build a graph of cross-links between articles."""
    articles = {}

    if not CONTENT_DIR.exists():
        return {"articles": {}, "orphan_count": 0}

    for json_path in CONTENT_DIR.rglob("*.json"):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        rel = str(json_path.relative_to(BASE_DIR))
        body = data.get("body", "")
        links = re.findall(r'href="([^"]*)"', body)
        articles[rel] = {
            "city": data.get("city", ""),
            "country": data.get("country", ""),
            "content_type": data.get("content_type", ""),
            "lang": data.get("lang", ""),
            "outgoing_links": links,
        }

    # Find orphans (articles with no incoming links)
    all_links = set()
    for art in articles.values():
        for link in art["outgoing_links"]:
            all_links.add(link)

    orphan_count = sum(1 for path in articles if path not in all_links)

    return {"articles": articles, "orphan_count": orphan_count}


def generate_report():
    """Generate a comprehensive project analysis report."""
    import re  # needed by analyze_internal_links

    print("=" * 60)
    print("PROJECT ANALYZER REPORT")
    print("=" * 60)

    # Coverage
    print("\n## Content Coverage")
    coverage = analyze_coverage()
    total_expected = 0
    total_generated = 0
    incomplete = []

    for slug, country in sorted(coverage.items()):
        pct = (country["total_generated"] / country["total_expected"] * 100
               if country["total_expected"] > 0 else 0)
        status = "✓" if pct == 100 else "⚠" if pct > 50 else "✗"
        print(f"  {status} {country['name_en']}: {country['total_generated']}/{country['total_expected']} ({pct:.0f}%)")
        total_expected += country["total_expected"]
        total_generated += country["total_generated"]

        for city_slug, city in country["cities"].items():
            for ct, data in city["types"].items():
                if not data["complete"]:
                    incomplete.append(f"    {city['name_en']}/{ct} ({data['generated']}/{data['expected']})")

    print(f"\n  Total: {total_generated}/{total_expected} ({total_generated/total_expected*100:.0f}%)")
    if incomplete:
        print(f"\n  Missing content ({len(incomplete)}):")
        for item in incomplete[:20]:
            print(item)
        if len(incomplete) > 20:
            print(f"    ... and {len(incomplete) - 20} more")

    # Staleness
    print("\n## Content Staleness")
    stale = analyze_staleness()
    if stale:
        print(f"  {len(stale)} articles older than 30 days:")
        for item in stale[:10]:
            print(f"    {item['path']} — {item['age_days']} days old (last modified: {item['modified']})")
    else:
        print("  All articles are recent.")

    # Affiliate coverage
    print("\n## Affiliate Coverage")
    aff = analyze_affiliate_coverage()
    if aff:
        avg = sum(a["count"] for a in aff) / len(aff)
        low = [a for a in aff if a["count"] < 3]
        print(f"  Average affiliate categories per article: {avg:.1f}")
        print(f"  Articles with <3 affiliate categories: {len(low)}")
        if low:
            for item in low[:5]:
                print(f"    {item['path']} — {item['count']} categories")

    # Internal links
    print("\n## Internal Links")
    links = analyze_internal_links()
    print(f"  Total articles: {len(links['articles'])}")
    print(f"  Orphan articles (no incoming links): {links['orphan_count']}")

    # Priorities
    print("\n## Priority Actions")
    priorities = []
    if incomplete:
        priorities.append(f"1. Generate missing content: {len(incomplete)} articles")
    if stale:
        priorities.append(f"2. Update stale content: {len(stale)} articles")
    if low:
        priorities.append(f"3. Add affiliate links: {len(low)} under-linked articles")
    if links["orphan_count"] > 0:
        priorities.append(f"4. Fix orphan articles: {links['orphan_count']} articles")
    if not priorities:
        print("  No critical issues found.")
    else:
        for p in priorities:
            print(f"  {p}")

    return {
        "coverage": coverage,
        "stale": stale,
        "affiliate_coverage": aff,
        "internal_links": links,
    }


def _get_content_slug(content_type, city_slug, lang):
    """Generate the content slug matching seo_optimizer.get_url_slug()."""
    slugs = {
        "guide": "putevoditel" if lang == "ru" else "travel-guide",
        "hotels": "oteli" if lang == "ru" else "hotels",
        "flights": "aviabilety" if lang == "ru" else "flights",
        "attractions": "dostoprimechatelnosti" if lang == "ru" else "attractions",
        "seasons": "kogda-luchshe-ekhat" if lang == "ru" else "best-time-to-visit",
    }
    return f"{city_slug}-{slugs.get(content_type, content_type)}"


if __name__ == "__main__":
    import sys
    if "--deep" in sys.argv:
        generate_report()
    else:
        coverage = analyze_coverage()
        for slug, country in sorted(coverage.items()):
            pct = (country["total_generated"] / country["total_expected"] * 100
                   if country["total_expected"] > 0 else 0)
            print(f"{slug}: {country['total_generated']}/{country['total_expected']} ({pct:.0f}%)")
