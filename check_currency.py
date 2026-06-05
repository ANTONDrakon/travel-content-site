import json, re
from pathlib import Path

CONTENT = Path(__file__).parent / "content"
found = []

for lang in ['ru', 'en']:
    base = CONTENT / lang
    for cf in sorted(base.glob('*/*.json')):
        with open(cf, encoding='utf-8') as fh:
            data = json.load(fh)
        body = data.get('body', '')
        keywords = ['курс', 'обмен', '1 TRY', '1 THB', '1 EGP', '1 AED', '1 CNY', '1 IDR', '1 MVR',
                     'лира ≈', 'бат ≈', 'фунт ≈', 'дирхам ≈', 'юан ≈', 'рупи ≈', 'руфи ≈',
                     '1 доллар', '1 usd', 'exchange rate', 'lira ≈', 'baht ≈', 'yuan ≈']
        for kw in keywords:
            if re.search(kw, body, re.IGNORECASE):
                found.append(f'{lang}/{cf.parent.name}/{cf.name} -> {kw}')
                break

print(f'Found {len(found)} files with potential currency mentions')
for f in found[:50]:
    print(f'  {f}')

# Now show actual currency snippets from 3 sample files
print('\n--- Sample snippets ---')
for cf_path in [
    'content/ru/turkey/istanbul-putevoditel.json',
    'content/en/turkey/istanbul-travel-guide.json',
    'content/ru/thailand/bangkok-putevoditel.json',
]:
    path = Path(__file__).parent / cf_path
    if path.exists():
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        body = data.get('body', '')
        # Find chunks with currency mentions
        for m in re.finditer(r'(?:1\s*(?:доллар|usd|лира|бат|TRY|THB|EGP|AED|CNY)[^<]{0,200})', body, re.IGNORECASE):
            print(f'\n  {cf_path}:')
            print(f'    {m.group(0)[:150]}')
            break
