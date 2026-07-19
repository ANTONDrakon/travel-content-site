"""
AGENT 2 — Content Architect
Designs content hierarchy and strategy: what to generate, in what order, with what priority.
"""
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"


def plan_content_hierarchy(country_slug=None):
    """For a country/city, determine which content types to generate and in what order."""
    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    plan = []

    countries = {country_slug: DESTINATIONS[country_slug]} if country_slug else DESTINATIONS

    for c_slug, dest in countries.items():
        # Handle both old structure (cities) and new structure (regions -> cities)
        cities = dest.get("cities", {})
        if not cities:
            for region_data in dest.get("regions", {}).values():
                cities.update(region_data.get("cities", {}))

        for city_slug, city in cities.items():
            for ct_slug, ct_info in sorted(CONTENT_TYPES.items(), key=lambda x: x[1]["priority"]):
                for lang in ["ru", "en"]:
                    content_path = _get_content_path(c_slug, city_slug, ct_slug, lang)
                    exists = content_path.exists()

                    plan.append({
                        "country": c_slug,
                        "country_name": dest["name_en"],
                        "city": city_slug,
                        "city_name": city["name_en"],
                        "content_type": ct_slug,
                        "lang": lang,
                        "priority": ct_info["priority"],
                        "exists": exists,
                        "path": str(content_path.relative_to(BASE_DIR)) if exists else None,
                    })

    return plan


def validate_hierarchy():
    """Ensure countries > cities > content types structure is correct."""
    from config.destinations import DESTINATIONS
    from config.prompts import CONTENT_TYPES

    issues = []

    for c_slug, dest in DESTINATIONS.items():
        if not dest.get("cities"):
            issues.append(f"EMPTY_COUNTRY: {c_slug} has no cities defined")

        for city_slug, city in dest.get("cities", {}).items():
            if not city.get("name_en") or not city.get("name_ru"):
                issues.append(f"MISSING_NAMES: {c_slug}/{city_slug} missing name_en or name_ru")

            if not city.get("airport_codes"):
                issues.append(f"NO_AIRPORT: {c_slug}/{city_slug} has no airport codes")

    return issues


def suggest_content_gaps(country_slug=None):
    """Suggest missing content types based on what's already generated."""
    plan = plan_content_hierarchy(country_slug)

    gaps = defaultdict(lambda: {"missing": [], "total_missing": 0})

    for item in plan:
        if not item["exists"]:
            key = f"{item['country']}/{item['city']}"
            gaps[key]["missing"].append({
                "content_type": item["content_type"],
                "lang": item["lang"],
                "priority": item["priority"],
            })
            gaps[key]["total_missing"] += 1

    # Sort by most missing first
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1]["total_missing"], reverse=True)

    return sorted_gaps


def generate_content_calendar(country_slug=None):
    """Ordered list of what to generate next, with priority scores."""
    plan = plan_content_hierarchy(country_slug)

    # Filter to missing content only
    missing = [p for p in plan if not p["exists"]]

    # Score by priority (lower number = higher priority) and language (RU first for Russian audience)
    for item in missing:
        score = item["priority"] * 10
        if item["lang"] == "ru":
            score -= 5  # Prioritize Russian content
        item["score"] = score

    missing.sort(key=lambda x: x["score"])

    return missing


def generate_report(country_slug=None):
    """Generate a content planning report."""
    print("=" * 60)
    print("CONTENT ARCHITECT REPORT")
    print("=" * 60)

    # Hierarchy validation
    print("\n## Hierarchy Validation")
    issues = validate_hierarchy()
    if issues:
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("  ✓ Hierarchy is valid")

    # Content gaps
    print("\n## Content Gaps")
    gaps = suggest_content_gaps(country_slug)
    total_missing = sum(g["total_missing"] for _, g in gaps)

    print(f"  Total missing articles: {total_missing}")
    print(f"\n  Top gaps (cities with most missing content):")
    for key, data in gaps[:15]:
        types = [f"{m['content_type']}({m['lang']})" for m in data["missing"]]
        print(f"    {key}: {data['total_missing']} missing — {', '.join(types)}")

    # Content calendar
    print("\n## Generation Priority (next 20)")
    calendar = generate_content_calendar(country_slug)
    for i, item in enumerate(calendar[:20]):
        print(f"  {i+1}. {item['country']}/{item['city']}/{item['content_type']}[{item['lang']}] (score: {item['score']})")

    # Statistics
    print("\n## Statistics")
    plan = plan_content_hierarchy(country_slug)
    total = len(plan)
    generated = sum(1 for p in plan if p["exists"])
    print(f"  Total possible articles: {total}")
    print(f"  Already generated: {generated}")
    print(f"  Remaining: {total - generated}")
    print(f"  Completion: {generated/total*100:.1f}%")

    return {
        "issues": issues,
        "gaps": gaps,
        "calendar": calendar,
        "stats": {"total": total, "generated": generated, "remaining": total - generated},
    }


def _get_content_path(country_slug, city_slug, content_type, lang):
    """Get the expected content JSON path using the same slug logic as seo_optimizer."""
    from agents.seo_optimizer import get_url_slug
    slug = get_url_slug(content_type, city_slug, lang)
    return CONTENT_DIR / lang / country_slug / f"{slug}.json"


if __name__ == "__main__":
    import sys
    country = sys.argv[1] if len(sys.argv) > 1 else None
    generate_report(country)
