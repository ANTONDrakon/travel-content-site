from pathlib import Path
import re

DOCS = Path(__file__).parent.parent / "docs"

def check_ux(path):
    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except:
        return [f"READ_ERROR: {path}"]
    
    if "viewport" not in html:
        issues.append("UX: MISSING viewport meta tag")
    
    if "@media" not in html:
        issues.append("UX: NO mobile media queries")
    
    cta_count = len(re.findall(r'(?:btn-cta|btn-outline|partner-btn|city-btn|Забронировать|Book now|Подобрать тур|Send Request)', html))
    if cta_count < 2:
        issues.append(f"UX: Too few CTAs ({cta_count})")
    
    imgs = re.findall(r'<img[^>]*>', html)
    img_no_lazy = [i for i in imgs if 'loading="lazy"' not in i and 'loading=' not in i]
    if len(img_no_lazy) > 3:
        issues.append(f"UX: {len(img_no_lazy)} images without lazy loading")
    
    if "position:fixed" not in html and "position: fixed" not in html:
        issues.append("UX: No fixed/sticky elements (scroll-to-top missing?)")
    
    return issues

def run():
    print("\n=== UX PERFORMANCE AGENT ===\n")
    total = 0
    for f in DOCS.rglob("*.html"):
        issues = check_ux(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues: print(f"  {i}"); total += 1
    print(f"\nTotal UX issues: {total}")
    return total

if __name__ == "__main__":
    run()
