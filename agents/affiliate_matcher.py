import re

def replace_placeholders(body, city_name_en, lang):
    from config.affiliates import (
        hotels_link, flights_link, tours_link, insurance_link,
        AFFILIATE_HTML, PLACEHOLDERS,
    )
    from config.destinations import DESTINATIONS

    city_slug = city_name_en.lower().replace(" ", "-")

    # Look up proper IATA airport code for the city
    destination_code = city_name_en.upper()[:3]
    for country in DESTINATIONS.values():
        for c_slug, city_data in country.get("cities", {}).items():
            if city_data.get("name_en", "").lower() == city_name_en.lower():
                codes = city_data.get("airport_codes", [])
                if codes:
                    destination_code = codes[0]
                break

    replacements = {
        "{hotels_placeholder}": AFFILIATE_HTML["hotels_en" if lang == "en" else "hotels"].format(
            url=hotels_link(city_slug), city=city_name_en
        ),
        "{flights_placeholder}": AFFILIATE_HTML["flights_en" if lang == "en" else "flights"].format(
            url=flights_link(destination=destination_code), city=city_name_en
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
    insurance_html = AFFILIATE_HTML["insurance_en" if lang == "en" else "insurance"].format(url=insurance_link())
    insurance_block = f'\n<div class="affiliate-block"><p>{"Don\'t forget travel insurance!" if lang == "en" else "Не забудьте оформить страховку для путешествия!"}</p>{insurance_html}</div>\n'

    # Find safe insertion point: after the last </p> or </h2> in the second half of body
    # This avoids breaking mid-paragraph text
    last_h2 = body.rfind("</h2>")
    last_p = body.rfind("</p>")
    insert_after = max(last_h2, last_p)

    if insert_after != -1 and insert_after > len(body) // 2:
        close_bracket = body.find(">", insert_after)
        if close_bracket != -1:
            body = body[:close_bracket + 1] + insurance_block + body[close_bracket + 1:]
        else:
            body = body[:insert_after] + insurance_block + body[insert_after:]
    else:
        body += insurance_block
    return body


def process_article_body(body, city_name_en, lang):
    body = replace_placeholders(body, city_name_en, lang)
    body = inject_insurance_block(body, lang)
    return body
