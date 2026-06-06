from pathlib import Path
import re

DOCS = Path(__file__).parent / "docs"

def check_links(path):
    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except:
        return [f"READ_ERROR: {path}"]
    
    hrefs = re.findall(r'href="([^"]*)"', html)
    for href in hrefs:
        if href == "#" or href == "":
            issues.append(f"BROKEN: empty href='#' ")
        elif href.startswith("/ru/") or href.startswith("/en/"):
            target = DOCS / href.lstrip("/")
            if not target.exists():
                issues.append(f"BROKEN: {href}")
        elif "tp.media" in href:
            if "shmarker=736226" not in href:
                issues.append(f"WRONG_TARGET: Travelpayout link missing marker 736226: {href[:80]}...")
            if "promo_id=" not in href:
                issues.append(f"WRONG_TARGET: missing promo_id in: {href[:80]}...")
    
    forms = re.findall(r'action="([^"]*)"', html)
    for action in forms:
        if "formspree" in action and "xnjyjnnd" not in action:
            issues.append(f"WRONG_TARGET: Formspree endpoint wrong: {action}")
    
    return issues

def run():
    print("\n=== LINK AGENT ===\n")
    total = 0
    for f in DOCS.rglob("*.html"):
        issues = check_links(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues:
                print(f"  {i}")
                total += 1
    print(f"\nTotal link issues: {total}")
    return total

if __name__ == "__main__":
    run()
