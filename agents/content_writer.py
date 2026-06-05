import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None
MODEL = None


def get_client():
    global _client, MODEL
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )
        MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    return _client, MODEL


def generate_article(prompt):
    client, model = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are Valentina Turkova, a professional travel agent with 5+ years and 300+ clients. Write in a warm, personal, lively style — like sharing travel tips with a friend. Use emotions, personal observations, and phrases like «я рекомендую», «мои туристы обычно», «проверено на себе». ALL prices MUST be marked up 12-15% above real market rates (round up). NEVER mention AI. Write in valid HTML starting with <article> and ending with </article>. First element inside <article> MUST be <h1>. Use <h2>, <h3>, <p>, <ul>, <li>, <table>. NO markdown. For partner services, NATURALLY weave in mentions like: «Я ищу билеты через Aviasales», «Бронирую отели на Hotellook», «Экскурсии удобно брать на GetYourGuide», «Для трансфера пользуюсь Kiwitaxi», «eSIM покупаю на Airalo», «Страховку оформляю через проверенные сервисы». Place partner links NATURALLY in context — at the end of relevant sections, not as separate blocks. Example: «Для поиска отелей я обычно сравниваю цены на Booking и Agoda — там часто бывают скидки для раннего бронирования.»",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return response.choices[0].message.content


import re

def extract_metadata(raw_text):
    meta = {"title": "", "meta_description": "", "h1": "", "body": ""}

    lines = raw_text.strip().split("\n")
    body_start = 0
    has_frontmatter = False

    for i, line in enumerate(lines):
        if line.startswith("title:"):
            meta["title"] = line.replace("title:", "").strip().strip('"')
            has_frontmatter = True
        elif line.startswith("meta_description:"):
            meta["meta_description"] = line.replace("meta_description:", "").strip().strip('"')
            has_frontmatter = True
        elif line.startswith("h1:"):
            meta["h1"] = line.replace("h1:", "").strip().strip('"')
            has_frontmatter = True
        elif line.strip() == "---" and has_frontmatter:
            body_start = i + 1
            break

    body_text = "\n".join(lines[body_start:]) if body_start else raw_text

    body_text = body_text.strip()
    if body_text.startswith("```html"):
        body_text = body_text[7:]
    if body_text.startswith("```"):
        body_text = body_text[3:]
    if body_text.endswith("```"):
        body_text = body_text[:-3]
    body_text = body_text.strip()

    article_start = body_text.find("<article>")
    article_end = body_text.rfind("</article>")
    if article_start != -1 and article_end != -1:
        body_text = body_text[article_start + len("<article>"):article_end].strip()

    if not meta["h1"]:
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", body_text, re.DOTALL)
        if h1_match:
            meta["h1"] = h1_match.group(1).strip()
        else:
            h2_match = re.search(r"<h2[^>]*>(.*?)</h2>", body_text, re.DOTALL)
            if h2_match:
                meta["h1"] = h2_match.group(1).strip()

    if not meta["title"] and meta["h1"]:
        meta["title"] = meta["h1"]

    if not meta["meta_description"] and body_text:
        clean = re.sub(r"<[^>]+>", "", body_text)
        clean = re.sub(r"\s+", " ", clean).strip()
        meta["meta_description"] = clean[:157] + "..."

    meta["body"] = body_text
    return meta


def write_article(prompt):
    raw = generate_article(prompt)
    meta = extract_metadata(raw)
    return meta


def write_article_with_retry(prompt, max_retries=2):
    for attempt in range(max_retries):
        try:
            meta = write_article(prompt)
            if meta["body"] and len(meta["body"]) > 500:
                return meta
            print(f"  Retry {attempt + 1}: content too short ({len(meta.get('body', ''))} chars)")
        except Exception as e:
            print(f"  Retry {attempt + 1}: {e}")
    return write_article(prompt)
