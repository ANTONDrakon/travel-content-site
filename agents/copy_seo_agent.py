from pathlib import Path
import re

DOCS = Path(__file__).parent / "docs"

def check_seo(path):
    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except:
        return [f"READ_ERROR: {path}"]
    
    title_m = re.search(r"<title>(.*?)</title>", html)
    if title_m:
        title = title_m.group(1)
        if len(title) < 20: issues.append("SEO: title too short (<20 chars)")
        if len(title) > 70: issues.append("SEO: title too long (>70 chars)")
    else:
        issues.append("SEO: MISSING <title>")
    
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not desc_m: issues.append("SEO: MISSING meta description")
    elif len(desc_m.group(1)) < 50: issues.append("SEO: meta description too short")
    elif len(desc_m.group(1)) > 165: issues.append("SEO: meta description too long")
    
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html)
    if len(h1s) == 0: issues.append("SEO: MISSING H1")
    elif len(h1s) > 1: issues.append(f"SEO: multiple H1 ({len(h1s)})")
    
    if "hreflang" not in html: issues.append("SEO: MISSING hreflang")
    if "canonical" not in html: issues.append("SEO: MISSING canonical")
    if "application/ld+json" not in html: issues.append("SEO: MISSING schema.org JSON-LD")
    if "og:title" not in html: issues.append("SEO: MISSING OpenGraph tags")
    
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 200: issues.append(f"SEO: content too short ({len(text)} chars)")
    
    return issues

def run():
    print("\n=== COPY SEO AGENT ===\n")
    total = 0
    for f in DOCS.rglob("*putevoditel*.html"):
        issues = check_seo(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues: print(f"  {i}"); total += 1
    for f in DOCS.rglob("*travel-guide*.html"):
        issues = check_seo(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues: print(f"  {i}"); total += 1
    print(f"\nTotal SEO issues: {total}")
    return total

if __name__ == "__main__":
    run()
