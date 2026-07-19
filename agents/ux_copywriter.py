"""
AGENT 8 — UX Copywriter
AI-driven content polish: readability, CTA optimization, AI fingerprint removal.
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"

# AI phrases to remove or replace
AI_PHRASES_RU = [
    (r"В заключение[,!]?\s*", ""),
    (r"Подводя итог[,!]?\s*", ""),
    (r"В завершение[,!]?\s*", ""),
    (r"Резюмируя[,!]?\s*", ""),
    (r"Таким образом[,!]?\s*", ""),
    (r"В целом[,!]?\s*", ""),
    (r"Стоит отметить,?\s*что\s+", ""),
    (r"Важно подчеркнуть,?\s*что\s+", ""),
    (r"Необходимо учитывать,?\s*что\s+", ""),
    (r"Следует обратить внимание,?\s*что\s+", ""),
    (r"Кроме того,?\s*", ""),
    (r"Более того,?\s*", ""),
    (r"Помимо этого,?\s*", ""),
    (r"Нельзя не отметить,?\s*что\s+", ""),
    (r"Безусловно,?\s*", ""),
    (r"Неоспоримо,?\s*", ""),
    (r"Факт(?:ом)?\s+остаётся,?\s*что\s+", ""),
    (r"Ключевым моментом является\s+", ""),
    (r"Основным преимуществом является\s+", ""),
]

AI_PHRASES_EN = [
    (r"In conclusion,?\s*", ""),
    (r"To sum up,?\s*", ""),
    (r"To conclude,?\s*", ""),
    (r"It is worth noting that\s+", ""),
    (r"It should be emphasized that\s+", ""),
    (r"Furthermore,?\s*", ""),
    (r"Moreover,?\s*", ""),
    (r"In addition,?\s*", ""),
    (r"Additionally,?\s*", ""),
    (r"It is important to mention that\s+", ""),
    (r"Undoubtedly,?\s*", ""),
    (r"Without a doubt,?\s*", ""),
    (r"The fact remains that\s+", ""),
    (r"A key point is\s+", ""),
    (r"The main advantage is\s+", ""),
    (r"Last but not least,?\s*", ""),
    (r"All things considered,?\s*", ""),
    (r"With that said,?\s*", ""),
]

# CTA templates
CTA_TEMPLATES_RU = {
    "tours": "Готовы к поездке? Подберите лучший тур прямо сейчас!",
    "hotels": "Забронируйте отель по лучшей цене уже сегодня!",
    "flights": "Ищите билеты? Начните поиск и сэкономьте!",
    "insurance": "Оформите страховку за 2 минуты — это проще, чем кажется!",
    "excursions": "Забронируйте экскурсию онлайн — никаких очередей!",
    "transfers": "Закажите трансфер заранее — начните поездку без стресса!",
    "default": "Начните планировать поездку прямо сейчас!",
}

CTA_TEMPLATES_EN = {
    "tours": "Ready to go? Find the best tour deal today!",
    "hotels": "Book your hotel at the best price — start now!",
    "flights": "Looking for flights? Search and save!",
    "insurance": "Get travel insurance in 2 minutes — it's easier than you think!",
    "excursions": "Book excursions online — no queues!",
    "transfers": "Pre-book your transfer — start your trip stress-free!",
    "default": "Start planning your trip right now!",
}


def remove_ai_fingerprints(body, lang="ru"):
    """Remove common AI-generated phrases and patterns."""
    phrases = AI_PHRASES_RU if lang == "ru" else AI_PHRASES_EN

    for pattern, replacement in phrases:
        body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)

    # Remove double spaces after removal
    body = re.sub(r'  +', ' ', body)

    # Fix sentence starts after removal (capitalize first letter)
    body = re.sub(r'([.!?]\s+)([а-яa-z])', lambda m: m.group(1) + m.group(2).upper(), body)

    return body


def validate_structure(body):
    """Check H2/H3 hierarchy, paragraph lengths, list formatting."""
    issues = []

    # Check heading hierarchy
    headings = re.findall(r'<h([123])>(.*?)</h\1>', body)
    prev_level = 0
    for level_str, text in headings:
        level = int(level_str)
        if level > prev_level + 1 and prev_level > 0:
            issues.append(f"HEADING_HIERARCHY: h{prev_level} → h{level} skip (text: {text[:50]})")
        prev_level = level

    # Check for very long paragraphs (>500 chars without line breaks)
    paragraphs = re.findall(r'<p>(.*?)</p>', body, re.DOTALL)
    for i, p in enumerate(paragraphs):
        clean = re.sub(r'<[^>]+>', '', p)
        if len(clean) > 500:
            issues.append(f"LONG_PARAGRAPH: Paragraph {i+1} is {len(clean)} chars — consider breaking it up")

    # Check for orphan headings (heading with no content after)
    # Only flag if H2 is followed by H2, or H3 is followed by H3 (same level)
    # H2→H3 is legitimate hierarchy (category → item)
    for match in re.finditer(r'<h([23])>(.*?)</h\1>\s*<h\1>', body):
        level = match.group(1)
        heading_text = match.group(2)[:50]
        # Skip common navigation/table-of-contents headings
        skip_patterns = ['содержание', 'contents', 'навигация', 'navigation', 'таблица', 'table']
        if not any(p in heading_text.lower() for p in skip_patterns):
            issues.append(f"ORPHAN_HEADING: h{level} '{heading_text}'")

    return issues


def break_long_paragraphs(body, max_chars=500):
    """Automatically break long paragraphs into shorter ones at sentence boundaries.

    Handles HTML content inside paragraphs by working with the full HTML string.
    """
    def break_paragraph(match):
        full_tag = match.group(0)
        p_content = match.group(1)
        clean = re.sub(r'<[^>]+>', '', p_content)

        if len(clean) <= max_chars:
            return full_tag

        # Find sentence boundaries (. ! ?) followed by space or end
        # We need to find positions in the ORIGINAL html, not clean text
        sentence_ends = []
        i = 0
        clean_pos = 0
        while i < len(p_content):
            if p_content[i] in '.!?':
                # Check if this is followed by space or end
                next_char = p_content[i+1] if i+1 < len(p_content) else ' '
                if next_char in ' \n\t' or i+1 == len(p_content):
                    # Calculate clean text position up to this point
                    clean_before = len(re.sub(r'<[^>]+>', '', p_content[:i+1]))
                    sentence_ends.append((i+1, clean_before))
            i += 1

        if len(sentence_ends) < 2:
            return full_tag

        # Find the best split point (closest to middle)
        mid_clean = len(clean) // 2
        best_split = min(sentence_ends, key=lambda x: abs(x[1] - mid_clean))

        # Split the HTML content at this position
        split_html = p_content[:best_split[0]].rstrip()
        second_html = p_content[best_split[0]:].lstrip()

        # Rebuild as HTML paragraphs
        return f"<p>{split_html}</p>\n<p>{second_html}</p>"

    # Process each <p>...</p> block (allow nested tags)
    body = re.sub(r'<p>(.*?)</p>', break_paragraph, body, flags=re.DOTALL)
    return body


def check_cta_presence(body, lang="ru"):
    """Ensure CTA elements are present and well-placed."""
    issues = []

    # Check for affiliate links
    affiliate_count = len(re.findall(r'partner-link', body))

    # Check for CTA-like elements
    cta_patterns = ["забронируй", "найди", "посмотри", "сравни", "оформи", "закажи",
                    "book", "find", "check", "compare", "get", "order"]
    cta_count = sum(1 for p in cta_patterns if p.lower() in body.lower())

    if affiliate_count == 0:
        issues.append("NO_CTA: No affiliate links found — article has no monetization")
    elif cta_count == 0:
        issues.append("WEAK_CTA: Affiliate links present but no CTA text — add action-oriented language")

    # Check for list/table usage (good for readability)
    has_list = bool(re.search(r'<[ou]l>', body))
    has_table = bool(re.search(r'<table', body))

    if not has_list and not has_table:
        issues.append("NO_LISTS: No lists or tables found — add structured content for better readability")

    return issues


def enhance_readability(body, lang="ru"):
    """Suggest readability improvements without rewriting."""
    suggestions = []

    # Check average sentence length
    sentences = re.split(r'[.!?]+', body)
    clean_sentences = [re.sub(r'<[^>]+>', '', s).strip() for s in sentences if len(s.strip()) > 10]
    if clean_sentences:
        avg_len = sum(len(s) for s in clean_sentences) / len(clean_sentences)
        if avg_len > 150:
            suggestions.append(f"LONG_SENTENCES: Average sentence length is {avg_len:.0f} chars — consider shorter sentences")

    # Check for bullet points (good UX)
    bullet_count = len(re.findall(r'<li>', body))
    if bullet_count == 0:
        suggestions.append("NO_BULLETS: Consider adding bullet-point lists for key information")

    # Check heading density
    h2_count = len(re.findall(r'<h2>', body))
    word_count = len(re.sub(r'<[^>]+>', '', body).split())
    if word_count > 500 and h2_count < 3:
        suggestions.append("LOW_HEADING_DENSITY: Long article with few section headings — add more H2 sections")

    return suggestions


def run_checks(article_path):
    """Run all UX copywriter checks on a content JSON file."""
    try:
        with open(article_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"error": f"Cannot read {article_path}"}

    body = data.get("body", "")
    lang = data.get("lang", "ru")

    results = {
        "structure": validate_structure(body),
        "cta": check_cta_presence(body, lang),
        "readability": enhance_readability(body, lang),
        "ai_fingerprints_found": bool(re.search(
            r'(В заключение|Подводя итог|In conclusion|To sum up|Furthermore|Кроме того)',
            body, re.IGNORECASE
        )),
    }

    return results


def run():
    """Scan all content files and report UX issues."""
    print("\n=== UX COPYWRITER ===\n")
    total_issues = 0

    if not CONTENT_DIR.exists():
        print("No content directory found.")
        return 0

    for json_path in sorted(CONTENT_DIR.rglob("*.json")):
        results = run_checks(json_path)
        if "error" in results:
            continue

        all_issues = results["structure"] + results["cta"] + results["readability"]
        if results["ai_fingerprints_found"]:
            all_issues.append("AI_FINGERPRINT: Contains common AI-generated phrases")

        if all_issues:
            rel = json_path.relative_to(BASE_DIR)
            print(f"\n[{rel}]")
            for issue in all_issues:
                print(f"  {issue}")
                total_issues += 1

    print(f"\nTotal issues: {total_issues}")
    return total_issues


if __name__ == "__main__":
    run()
