import re
from pathlib import Path

BASE = Path(__file__).parent / "docs"

# Check Maldives
maldives_html = BASE / "ru" / "maldives" / "index.html"
if maldives_html.exists():
    h = maldives_html.read_text(encoding="utf-8")
    t = re.search(r'<title>(.*?)</title>', h)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h)
    if t and h1:
        print(f'Maldives RU title: {t.group(1)}')
        print(f'Maldives RU h1: {h1.group(1)}')
        print(f'PASS: {"на Мальдивах" in t.group(1) and "на Мальдивах" in h1.group(1)}')
    else:
        print("Maldives RU: title or h1 not found")
else:
    print(f"Maldives RU page not found: {maldives_html}")

# Check homepage hreflang
home_html = BASE / "ru" / "index.html"
if home_html.exists():
    h = home_html.read_text(encoding="utf-8")
    hrefs = re.findall(r'hreflang="(.*?)".*?href="(.*?)"', h)
    print(f'\nHomepage hreflangs:')
    for lang, url in hrefs:
        ok = '/ru/ru/' not in url and '/en/ru/' not in url
        print(f'  {lang}: {url} - {"OK" if ok else "FAIL - double prefix"}')
else:
    print(f"Homepage not found: {home_html}")
