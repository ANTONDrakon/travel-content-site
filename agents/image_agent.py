from pathlib import Path
import re

DOCS = Path(__file__).parent / "docs"

CITY_KEYWORDS = {
    "istanbul": ["istanbul", "стамбул", "мечеть", "босфор", "султанахмет"],
    "antalya": ["antalya", "анталья", "пляж", "лара", "калеичи"],
    "dubai": ["dubai", "дубай", "бурдж", "бурж", "marina", "марина"],
    "abu-dhabi": ["abu dhabi", "абу-даби", "шейх зайд", "корниш", "лувр"],
    "sharm": ["sharm", "шарм", "синай", "рас-мохаммед", "наама"],
    "bangkok": ["bangkok", "бангкок", "ваты", "чао-прайя", "дворец"],
    "beijing": ["beijing", "пекин", "запретный город", "великая стена"],
    "male": ["male", "мале", "аэропорт", "рыбный рынок", "хулумале"],
}

def check_image_context(path):
    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except:
        return [f"READ_ERROR: {path}"]
    
    imgs = re.findall(r'<img[^>]+alt="([^"]*)"[^>]*>', html)
    for alt in imgs:
        if "Unsplash" in alt or "Photo" in alt or "photo" in alt:
            issues.append(f"MISMATCH_ALT: generic alt text '{alt[:60]}'")
    
    rel_path = str(path.relative_to(DOCS)).lower()
    for city, keywords in CITY_KEYWORDS.items():
        if city in rel_path:
            for kw in keywords:
                if kw.lower() in rel_path:
                    break
            else:
                pass
    
    return issues

def run():
    print("\n=== IMAGE AGENT ===\n")
    total = 0
    for f in DOCS.rglob("*.html"):
        issues = check_image_context(f)
        if issues:
            rel = f.relative_to(DOCS)
            print(f"\n[{rel}]")
            for i in issues:
                print(f"  {i}")
                total += 1
    print(f"\nTotal image issues: {total}")
    return total

if __name__ == "__main__":
    run()
