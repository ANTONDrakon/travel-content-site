"""Add currency disclaimer to all AI-generated articles with price mentions."""

import json
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "content"

DISCLAIMER_RU = (
    '<p style="font-size:14px;color:var(--meta);margin-bottom:16px;padding:12px 16px;'
    'background:var(--bg);border-radius:8px;">'
    '⚠️ Все цены и курсы валют в статье — ориентировочные на июнь 2026 года. '
    'Перед бронированием проверяйте актуальные цены и курс у турагента.</p>'
)

DISCLAIMER_EN = (
    '<p style="font-size:14px;color:var(--meta);margin-bottom:16px;padding:12px 16px;'
    'background:var(--bg);border-radius:8px;">'
    '⚠️ All prices and exchange rates in this article are approximate as of June 2026. '
    'Verify current rates and prices before booking.</p>'
)


def has_price_mentions(body):
    """Check if article mentions prices or money."""
    return bool(re.search(r'[\$₽€]\s*\d+|рубл|RUB|USD|доллар|бюджет|budget|цена|price|стоимост|cost|бесплатн',
                          body, re.IGNORECASE))


def already_has_disclaimer(body, lang):
    """Check if disclaimer is already present."""
    if lang == "ru":
        return "Все цены и курсы валют в статье — ориентировочные" in body
    return "All prices and exchange rates in this article are approximate" in body


def add_disclaimer(body, lang):
    """Insert disclaimer after the first <p> or after </h1>."""
    if already_has_disclaimer(body, lang):
        return body

    disclaimer = DISCLAIMER_RU if lang == "ru" else DISCLAIMER_EN

    # Try to insert after first </h1>
    h1_pos = body.find("</h1>")
    if h1_pos > 0:
        after_tag = body.find(">", h1_pos) + 1
        return body[:after_tag] + disclaimer + body[after_tag:]

    # Try after opening tag after first heading
    m = re.search(r'(<h1[^>]*>.*?</h1>\s*(?:<p[^>]*>.*?</p>\s*)?)', body)
    if m:
        return body[:m.end()] + disclaimer + body[m.end():]

    # Fallback: after first paragraph
    p_pos = body.find("</p>")
    if p_pos > 0:
        return body[:p_pos + 4] + disclaimer + body[p_pos + 4:]

    return body


def fix_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False

    body = data.get("body", "")
    if not body:
        return False

    lang = "ru" if "/ru/" in str(filepath) else "en"

    if not has_price_mentions(body):
        return False

    if already_has_disclaimer(body, lang):
        return False

    data["body"] = add_disclaimer(body, lang)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def main():
    print("Adding currency disclaimers to articles...")
    fixed = 0
    skipped = 0
    total = 0

    for lang_dir in ["ru", "en"]:
        lang_path = CONTENT_DIR / lang_dir
        if not lang_path.exists():
            continue
        for country_dir in sorted(lang_path.iterdir()):
            if not country_dir.is_dir():
                continue
            for jf in sorted(country_dir.glob("*.json")):
                total += 1
                if fix_file(jf):
                    fixed += 1
                    print(f"  + {jf.relative_to(CONTENT_DIR)}")
                else:
                    skipped += 1

    print(f"\nDone: {fixed} updated, {skipped} skipped (no prices or already OK), {total} total files.")


if __name__ == "__main__":
    main()
