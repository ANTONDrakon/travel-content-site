MARKER = "736226"

def tp_link(campaign=101, promo=3772, trs="", link_type="click"):
    return f"https://tp.media/click?shmarker={MARKER}&promo_id={promo}&source_type=link&type={link_type}&campaign_id={campaign}&trs={trs}"

PARTNER_PROGRAMS = {
    "hotellook": ("Hotellook", tp_link(101, 3772, ""), "4–8%", "🔍"),
    "aviasales": ("Aviasales", tp_link(100, 3770, ""), "1.1–1.3%", "✈️"),
    "booking": ("Booking.com", "https://tp.media/click?shmarker=736226&promo_id=3776&source_type=link&type=click&campaign_id=108&trs={trs}", "3–5%", "🏨"),
    "agoda": ("Agoda", "https://tp.media/click?shmarker=736226&promo_id=3779&source_type=link&type=click&campaign_id=110&trs={trs}", "6%", "🏩"),
    "viator": ("Viator", "https://tp.media/click?shmarker=736226&promo_id=3775&source_type=link&type=click&campaign_id=107&trs={trs}", "8%", "🎫"),
    "getyourguide": ("GetYourGuide", "https://tp.media/click?shmarker=736226&promo_id=3798&source_type=link&type=click&campaign_id=115&trs={trs}", "8%", "🗺"),
    "discovercars": ("DiscoverCars", "https://tp.media/click?shmarker=736226&promo_id=3780&source_type=link&type=click&campaign_id=111&trs={trs}", "23–54%", "🚗"),
    "kiwitaxi": ("Kiwitaxi", "https://tp.media/click?shmarker=736226&promo_id=3782&source_type=link&type=click&campaign_id=112&trs={trs}", "9–11%", "🚕"),
    "airalo": ("Airalo eSIM", "https://tp.media/click?shmarker=736226&promo_id=3803&source_type=link&type=click&campaign_id=118&trs={trs}", "12%", "📶"),
    "localrent": ("Localrent", "https://tp.media/click?shmarker=736226&promo_id=3783&source_type=link&type=click&campaign_id=113&trs={trs}", "7.5–12%", "🏍"),
    "tiqets": ("Tiqets", "https://tp.media/click?shmarker=736226&promo_id=3801&source_type=link&type=click&campaign_id=116&trs={trs}", "3.5–8%", "🎟"),
    "compensair": ("Compensair", "https://tp.media/click?shmarker=736226&promo_id=3800&source_type=link&type=click&campaign_id=117&trs={trs}", "€5–12", "💸"),
    "kiwi": ("Kiwi.com", "https://tp.media/click?shmarker=736226&promo_id=3799&source_type=link&type=click&campaign_id=114&trs={trs}", "3%", "🛫"),
    "tripcom": ("Trip.com", "https://tp.media/click?shmarker=736226&promo_id=3802&source_type=link&type=click&campaign_id=119&trs={trs}", "1–5.5%", "🎒"),
    "klook": ("Klook", "https://tp.media/click?shmarker=736226&promo_id=3797&source_type=link&type=click&campaign_id=120&trs={trs}", "2–5%", "🎌"),
}

def partner_button(name, url_template, trs, icon=""):
    url = url_template.replace("{trs}", trs)
    return f'<a href="{url}" target="_blank" rel="nofollow sponsored" class="partner-btn">{icon} {name}</a>'

def get_hotel_links(city_en):
    trs = f"hotels_{city_en.lower().replace(' ', '_')}"
    links = []
    for key in ["hotellook", "booking", "agoda"]:
        name, url_tpl, rate, icon = PARTNER_PROGRAMS[key]
        links.append(partner_button(name, url_tpl, trs, icon))
    return " ".join(links)

def get_flight_links(destination_code):
    trs = f"flights_{destination_code}"
    links = []
    for key in ["aviasales", "kiwi", "tripcom"]:
        name, url_tpl, rate, icon = PARTNER_PROGRAMS[key]
        links.append(partner_button(name, url_tpl, trs, icon))
    return " ".join(links)

def get_tour_links(city_en):
    trs = f"tours_{city_en.lower().replace(' ', '_')}"
    links = []
    for key in ["viator", "getyourguide", "tiqets", "klook"]:
        name, url_tpl, rate, icon = PARTNER_PROGRAMS[key]
        links.append(partner_button(name, url_tpl, trs, icon))
    return " ".join(links)

def get_transfer_links(city_en):
    trs = f"transfer_{city_en.lower().replace(' ', '_')}"
    links = []
    for key in ["kiwitaxi", "discovercars", "localrent"]:
        name, url_tpl, rate, icon = PARTNER_PROGRAMS[key]
        links.append(partner_button(name, url_tpl, trs, icon))
    return " ".join(links)

PARTNER_CSS = """
.partner-btn {
    display: inline-block; padding: 10px 20px;
    border: 1.5px solid var(--vermillion); border-radius: 14px;
    color: var(--vermillion); font-size: 14px; font-weight: 520;
    text-decoration: none; margin: 6px 8px 6px 0;
    transition: all 0.2s; background: transparent;
}
.partner-btn:hover { background: var(--vermillion); color: #fff; }
.partner-block {
    background: #fff; padding: 24px; margin: 32px 0;
    border-radius: 16px; border-left: 4px solid var(--vermillion);
}
.partner-block h4 { font-size: 17px; font-weight: 700; margin-bottom: 12px; color: var(--ink); }
"""

def inject_partner_links(body, content_type, city_name_en, country_slug):
    block = ""

    if content_type == "hotels":
        block = f"""
        <div class="partner-block">
            <h4>🏨 Где забронировать отель в {city_name_en}</h4>
            <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">Я для своих туристов подбираю отели через эти сервисы — проверено, надёжно, с кэшбэком:</p>
            {get_hotel_links(city_name_en)}
        </div>
        """
    elif content_type == "flights":
        block = f"""
        <div class="partner-block">
            <h4>✈️ Где искать авиабилеты</h4>
            <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">Я всегда сравниваю цены в нескольких сервисах перед покупкой. Вот мои проверенные:</p>
            {get_flight_links(city_name_en[:3].upper())}
        </div>
        """
    elif content_type == "attractions":
        block = f"""
        <div class="partner-block">
            <h4>🎫 Экскурсии и билеты без очередей</h4>
            <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">Бронируйте входные билеты и экскурсии заранее — экономия до 30%:</p>
            {get_tour_links(city_name_en)}
        </div>
        """
    elif content_type == "guide":
        block = f"""
        <div class="partner-block">
            <h4>🔍 Искать отели в {city_name_en}</h4>
            {get_hotel_links(city_name_en)}
        </div>
        <div class="partner-block">
            <h4>✈️ Найти билеты</h4>
            {get_flight_links(city_name_en[:3].upper())}
        </div>
        <div class="partner-block">
            <h4>🎫 Экскурсии и развлечения</h4>
            {get_tour_links(city_name_en)}
        </div>
        """

    transfer_block = f"""
    <div class="partner-block">
        <h4>🚕 Трансфер и аренда авто</h4>
        <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">Закажите трансфер из аэропорта или арендуйте авто заранее:</p>
        {get_transfer_links(city_name_en)}
    </div>
    """

    insurance_block = f"""
    <div class="partner-block">
        <h4>🛡 Страховка путешественника</h4>
        <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">Никогда не путешествуйте без страховки. Я рекомендую оформить заранее:</p>
        {partner_button('Оформить страховку', 'https://tp.media/click?shmarker=736226&promo_id=3773&source_type=link&type=click&campaign_id=102&trs=insurance_{country_slug}', 'insurance_' + country_slug, '🛡')}
        <span style="margin-left:12px;font-size:13px;color:var(--meta);">от $5 за полное покрытие</span>
    </div>
    """

    sim_block = f"""
    <div class="partner-block">
        <h4>📶 Интернет в поездке</h4>
        <p style="color:var(--meta);font-size:14px;margin-bottom:12px;">eSIM с интернетом — подключите до вылета и оставайтесь на связи:</p>
        {partner_button('Airalo eSIM', 'https://tp.media/click?shmarker=736226&promo_id=3803&source_type=link&type=click&campaign_id=118&trs=airalo_{country_slug}', 'airalo_' + country_slug, '📶')}
    </div>
    """

    close_tag = "</article>"
    if close_tag in body:
        insert_pos = body.rfind(close_tag)
        body = body[:insert_pos] + block + transfer_block + insurance_block + sim_block + body[insert_pos:]
    else:
        body += block + transfer_block + insurance_block + sim_block

    return body
