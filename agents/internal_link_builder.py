"""
AGENT 7 — Internal Link Builder
Proactively builds internal linking strategy across all articles.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"


def build_link_graph():
    """Scan all articles, extract topics, cities, content types. Build a graph."""
    articles = {}

    if not CONTENT_DIR.exists():
        return articles

    for json_path in CONTENT_DIR.rglob("*.json"):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        rel = str(json_path.relative_to(BASE_DIR))
        body = data.get("body", "")

        # Extract keywords from headings
        headings = re.findall(r'<h[23]>(.*?)</h[23]>', body)

        # Extract existing internal links
        internal_links = re.findall(r'href="(/[^"]+)"', body)

        articles[rel] = {
            "path": json_path,
            "country": data.get("country", ""),
            "city": data.get("city", ""),
            "content_type": data.get("content_type", ""),
            "lang": data.get("lang", ""),
            "title": data.get("h1", data.get("title", "")),
            "headings": headings,
            "existing_links": internal_links,
        }

    return articles


def suggest_related(article_path, graph, max_results=8):
    """For a given article, suggest related articles by: same country, same content type, nearby cities, thematic overlap."""
    article = graph.get(article_path)
    if not article:
        return []

    candidates = []
    for path, other in graph.items():
        if path == article_path:
            continue
        if other["lang"] != article["lang"]:
            continue

        score = 0
        reasons = []

        # Same country = strong signal
        if other["country"] == article["country"]:
            score += 30
            reasons.append("same_country")

        # Same city but different content type = very strong
        if other["city"] == article["city"] and other["content_type"] != article["content_type"]:
            score += 50
            reasons.append("same_city_different_type")

        # Same content type in different city = moderate
        if other["content_type"] == article["content_type"] and other["city"] != article["city"]:
            score += 15
            reasons.append("same_content_type")

        # Heading keyword overlap
        art_words = set(" ".join(article["headings"]).lower().split())
        other_words = set(" ".join(other["headings"]).lower().split())
        overlap = len(art_words & other_words)
        if overlap > 2:
            score += min(overlap * 3, 20)
            reasons.append(f"heading_overlap_{overlap}")

        if score > 0:
            candidates.append({
                "path": path,
                "title": other["title"],
                "city": other["city"],
                "country": other["country"],
                "content_type": other["content_type"],
                "score": score,
                "reasons": reasons,
            })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:max_results]


def inject_related_section(article_path, graph, lang="ru"):
    """Add 'Related Articles' section at the end of an article."""
    related = suggest_related(article_path, graph, max_results=6)
    if not related:
        return None

    header = "Похожие статьи" if lang == "ru" else "Related Articles"
    links_html = []
    for r in related:
        href = "/" + r["path"].replace(".json", ".html")
        if f"/{lang}/" in href:
            href = href.split(f"/{lang}/", 1)[1]
        title = r["title"] or f"{r['city']} — {r['content_type']}"
        links_html.append(f'<li><a href="/{lang}/{href}">{title}</a></li>')

    section = f'\n<div class="related-articles">\n<h2>{header}</h2>\n<ul>\n'
    section += "\n".join(links_html)
    section += "\n</ul>\n</div>\n"
    return section


def inject_contextual_links(body, graph, current_path, lang="ru"):
    """Within article body, identify opportunities to add inline links to related content."""
    article = graph.get(current_path)
    if not article:
        return body

    # Find city names in body that could be linked
    cities_mentioned = set()
    for path, other in graph.items():
        if path == current_path:
            continue
        if other["lang"] != lang:
            continue
        city_name = other.get("city", "").replace("-", " ").title()
        if len(city_name) > 2 and city_name.lower() in body.lower():
            cities_mentioned.add((city_name, path))

    # Don't add if too many links already
    existing_link_count = len(re.findall(r'<a href=', body))
    if existing_link_count > 20:
        return body

    for city_name, path in cities_mentioned:
        href = "/" + path.replace(".json", ".html")
        if f"/{lang}/" in href:
            href = href.split(f"/{lang}/", 1)[1]
        # Only link first occurrence
        link_html = f'<a href="/{lang}/{href}">{city_name}</a>'
        pattern = re.compile(r'(?<!["\'>])(' + re.escape(city_name) + r')(?!["\'<a])', re.IGNORECASE)
        body = pattern.sub(link_html, body, count=1)

    return body


def generate_link_report():
    """Generate a report on internal link health."""
    graph = build_link_graph()

    print("=" * 60)
    print("INTERNAL LINK REPORT")
    print("=" * 60)

    total_articles = len(graph)
    articles_with_links = sum(1 for a in graph.values() if a["existing_links"])
    orphan_count = sum(1 for a in graph.values() if not a["existing_links"])

    print(f"\nTotal articles: {total_articles}")
    print(f"Articles with outgoing links: {articles_with_links}")
    print(f"Orphan articles (no outgoing links): {orphan_count}")

    # Country distribution
    by_country = defaultdict(list)
    for path, art in graph.items():
        by_country[art["country"]].append(path)

    print(f"\nArticles by country:")
    for country, paths in sorted(by_country.items()):
        print(f"  {country}: {len(paths)}")

    # Suggest improvements
    print(f"\nTop link opportunities:")
    opportunities = []
    for path, art in graph.items():
        related = suggest_related(path, graph, max_results=3)
        if related and len(art["existing_links"]) < 2:
            opportunities.append({
                "article": art["title"] or path,
                "missing_related": len(related),
                "top_related": [r["title"] for r in related[:3]],
            })

    opportunities.sort(key=lambda x: x["missing_related"], reverse=True)
    for opp in opportunities[:10]:
        print(f"  {opp['article']}")
        for rel in opp["top_related"]:
            print(f"    → {rel}")

    return graph


if __name__ == "__main__":
    import sys
    if "--report" in sys.argv:
        generate_link_report()
    else:
        graph = build_link_graph()
        print(f"Loaded {len(graph)} articles")
        for path, art in list(graph.items())[:5]:
            related = suggest_related(path, graph, max_results=3)
            print(f"\n{art['title'] or path}:")
            for r in related:
                print(f"  → {r['title']} (score: {r['score']}, {', '.join(r['reasons'])})")
