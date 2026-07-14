"""Fix broken hotel slugs in hotels.json."""
import json, re
from pathlib import Path

BASE = Path(__file__).parent
hotels = json.loads((BASE / "data" / "hotels.json").read_text(encoding="utf-8"))

fixed = 0
removed = 0
clean_hotels = []

for h in hotels:
    slug = h.get("slug", "")
    name = h.get("name", "")

    # Remove non-hotel entries (tips, sections)
    if slug in ["--", "-", ""] or name.startswith("Для ") or name.startswith("Как ") or name.startswith("Когда ") or name.startswith("Лучшие"):
        removed += 1
        continue

    # Fix double dashes in slugs
    new_slug = slug.replace("--", "-")
    if new_slug != slug:
        h["slug"] = new_slug
        fixed += 1

    clean_hotels.append(h)

# Write back
(BASE / "data" / "hotels.json").write_text(
    json.dumps(clean_hotels, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Removed {removed} non-hotel entries")
print(f"Fixed {fixed} broken slugs")
print(f"Total hotels: {len(clean_hotels)}")
