import re

def replace_placeholders(body, city_name_en, lang):
    from config.affiliates import (
        hotels_link, flights_link, tours_link, insurance_link,
        AFFILIATE_HTML, PLACEHOLDERS,
    )

    city_slug = city_name_en.lower().replace(" ", "-")

    replacements = {
        "{hotels_placeholder}": AFFILIATE_HTML["hotels_en" if lang == "en" else "hotels"].format(
            url=hotels_link(city_slug), city=city_name_en
        ),
        "{flights_placeholder}": AFFILIATE_HTML["flights_en" if lang == "en" else "flights"].format(
            url=flights_link(destination=city_name_en.upper()[:3]), city=city_name_en
        ),
        # TODO: use actual IATA codes from cities.json instead of first 3 chars
        "{tours_placeholder}": AFFILIATE_HTML["tours_en" if lang == "en" else "tours"].format(
            url=tours_link(city_name_en), city=city_name_en
        ),
    }

    for placeholder, html in replacements.items():
        body = body.replace(placeholder, html)

    return body


def inject_insurance_block(body, lang):
    from config.affiliates import insurance_link, AFFILIATE_HTML
    insurance_html = AFFILIATE_HTML["insurance_en" if lang == "en" else "insurance"].format(url=insurance_link())
    insurance_block = f'<div class="affiliate-banner"><p>{"Don\'t forget travel insurance!" if lang == "en" else "Не забудьте оформить страховку для путешествия!"}</p>{insurance_html}</div>'

    close_article = body.rfind("</article>")
    if close_article != -1:
        body = body[:close_article] + insurance_block + body[close_article:]
    else:
        body += insurance_block
    return body


def process_article_body(body, city_name_en, lang):
    body = replace_placeholders(body, city_name_en, lang)
    body = inject_insurance_block(body, lang)
    return body
