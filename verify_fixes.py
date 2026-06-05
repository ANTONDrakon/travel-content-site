import re

# Check Maldives 
with open(r'C:\Users\anttu\OneDrive\Рабочий стол\555\travel-content-factory\docs\ru\maldives\index.html', encoding='utf-8') as f:
    h = f.read()
t = re.search(r'<title>(.*?)</title>', h).group(1)
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h).group(1)
print(f'Maldives RU title: {t}')
print(f'Maldives RU h1: {h1}')
print(f'PASS: {"на Мальдивах" in t and "на Мальдивах" in h1}')

# Check homepage hreflang
with open(r'C:\Users\anttu\OneDrive\Рабочий стол\555\travel-content-factory\docs\ru\index.html', encoding='utf-8') as f:
    h = f.read()
hrefs = re.findall(r'hreflang="(.*?)".*?href="(.*?)"', h)
print(f'\nHomepage hreflangs:')
for lang, url in hrefs:
    ok = '/ru/ru/' not in url and '/en/ru/' not in url
    print(f'  {lang}: {url} - {"OK" if ok else "FAIL - double prefix"}')
