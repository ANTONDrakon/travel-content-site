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
        "{tours_placeholder}": AFFILIATE_HTML["tours_en" if lang == "en" else "tours"].format(
            url=tours_link(city_name_en), city=city_name_en
        ),
    }

    for placeholder, html in replacements.items():
        body = body.replace(placeholder, html)

    return body


def inject_insurance_block(body, lang):
    from config.affiliates import insurance_link, AFFILIATE_HTML

    insurance_html = AFFILIATE_HTML["insurance_en" if lang == "en" else "insurance"].format(
        url=insurance_link()
    )

    insurance_block = f'<div class="affiliate-banner"><p>{"Don\'t forget travel insurance!" if lang == "en" else "Не забудьте оформить страховку для путешествия!"}</p>{insurance_html}</div>'

    close_body = "</article>"
    if close_body not in body and "</div>" in body:
        last_div = body.rfind("</div>")
        body = body[:last_div] + insurance_block + body[last_div:]
    elif "</section>" in body:
        last_section = body.rfind("</section>")
        body = body[:last_section] + insurance_block + body[last_section:]
    else:
        body += insurance_block

    return body


def process_article_body(body, city_name_en, lang):
    body = replace_placeholders(body, city_name_en, lang)
    body = inject_insurance_block(body, lang)
    return body
