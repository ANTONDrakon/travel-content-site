from pathlib import Path
import json, re

DOCS = Path(__file__).parent / "docs"

KNOWN_FACTS = {
    "turkey": {"visa": "безвизовый до 90 дней", "currency": "турецкая лира (TRY)", "airports": ["IST", "SAW", "AYT"]},
    "thailand": {"visa": "безвизовый до 30 дней", "currency": "тайский бат (THB)", "airports": ["BKK", "HKT"]},
    "egypt": {"visa": "виза по прибытии $25", "currency": "египетский фунт (EGP)", "airports": ["SSH", "HRG", "CAI"]},
    "uae": {"visa": "безвизовый до 90 дней", "currency": "дирхам ОАЭ (AED)", "airports": ["DXB", "AUH"]},
    "indonesia": {"visa": "виза по прибытии", "currency": "индонезийская рупия (IDR)", "airports": ["DPS"]},
    "china": {"visa": "виза требуется, Хайнань — безвизовый", "currency": "китайский юань (CNY)", "airports": ["PEK", "PVG", "SYX"]},
    "maldives": {"visa": "бесплатная виза по прибытии 30 дней", "currency": "мальдивская руфия (MVR), USD", "airports": ["MLE"]},
}

SUSPICIOUS_PATTERNS = [
    (r"от €?\d[\d,.]*\s*(?:евро|€)", "Цена в евро без конвертации в ₽"),
    (r"население \d[\d,.]* млн", "Население без источника"),
    (r"входит в топ-\d", "Рейтинг без источника"),
    (r"самый (?:лучший|популярный|большой|красивый)", "Субъективная оценка без подтверждения"),
    (r"гарантированно|100% гаранти|наверняка", "Гарантия без оснований"),
]

def check_article(path):
    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except:
        return [f"READ_ERROR: {path}"]
    
    for pattern, desc in SUSPICIOUS_PATTERNS:
        if re.search(pattern, html, re.IGNORECASE):
            issues.append(f"UNVERIFIED: {desc}")
    
    counts = {"₽": len(re.findall(r'₽', html)), "$": len(re.findall(r'\$\d', html)),
              "€": len(re.findall(r'€\d', html))}
    if counts["€"] > 0 and counts["₽"] < counts["€"]:
        issues.append("PRICE_FORMAT: больше цен в € чем в ₽")
    
    return issues

def run():
    print("\n=== FACT AGENT ===\n")
    total_issues = 0
    for f in DOCS.rglob("*putevoditel*.html"):
        issues = check_article(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues:
                print(f"  {i}")
                total_issues += 1
    
    for f in DOCS.rglob("*travel-guide*.html"):
        issues = check_article(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues:
                print(f"  {i}")
                total_issues += 1
    
    print(f"\nTotal issues: {total_issues}")
    return total_issues

if __name__ == "__main__":
    run()
