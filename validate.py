import os, sys, json, re
from pathlib import Path

BASE = Path(__file__).parent
CONTENT = BASE / "content"
DOCS = BASE / "docs"

def check_images_in_file(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    issues = []
    for img in imgs:
        fn = Path(img).name if "/" in img else img
        if "unsplash" in img:
            pid = re.search(r'photo-([a-zA-Z0-9_-]+)', img)
            if not pid:
                issues.append(f"  BAD Unsplash URL: {img[:80]}")
    if not imgs:
        issues.append("  NO IMAGES found")
    return issues

def check_all():
    errors = []
    for html_file in DOCS.rglob("*.html"):
        rel = html_file.relative_to(DOCS)
        page_issues = check_images_in_file(html_file)
        if page_issues:
            errors.append(f"\n[{rel}]")
            errors.extend(page_issues)

    for country_dir in CONTENT.rglob("*"):
        if country_dir.is_dir():
            jsons = list(country_dir.glob("*.json"))
            if jsons and len(jsons) < 5:
                name = country_dir.relative_to(CONTENT)
                errors.append(f"\n[INCOMPLETE dir: {name}] {len(jsons)}/5 articles")

    output = "\n".join(errors) if errors else "ALL CLEAN - No issues found"
    print(f"\n=== Site Validation Report ===\n{output}\n=== End Report ===")

def check_broken_imgs():
    from config.destinations import DESTINATIONS
    from publisher import CITY_IMAGES, COUNTRY_IMAGES

    all_slugs = set()
    for cs, country in DESTINATIONS.items():
        all_slugs.add(cs)
        for city_slug in country["cities"]:
            all_slugs.add(city_slug)

    missing = []
    for cs in DESTINATIONS:
        if cs not in COUNTRY_IMAGES:
            missing.append(f"  MISSING country image: {cs}")
        for city_slug in DESTINATIONS[cs]["cities"]:
            if city_slug not in CITY_IMAGES:
                missing.append(f"  MISSING city image: {city_slug}")

    if missing:
        print("\n=== Missing Images ===\n" + "\n".join(missing))
    else:
        print("\n=== All images present ===")

if __name__ == "__main__":
    check_all()
    check_broken_imgs()
