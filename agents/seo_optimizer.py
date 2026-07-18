SLUGS_RU = {
    "guide": "putevoditel",
    "hotels": "oteli",
    "flights": "aviabilety",
    "attractions": "dostoprimechatelnosti",
    "seasons": "kogda-luchshe-ekhat",
}

SLUGS_EN = {
    "guide": "travel-guide",
    "hotels": "hotels",
    "flights": "cheap-flights",
    "attractions": "things-to-do",
    "seasons": "best-time-to-visit",
}


def get_url_slug(content_type, city_slug, lang):
    if lang == "ru":
        type_slug = SLUGS_RU.get(content_type, content_type)
    else:
        type_slug = SLUGS_EN.get(content_type, content_type)
    return f"{city_slug}-{type_slug}"


def build_seo_meta(article_meta, city_slug, country_slug, content_type, lang):
    slug = get_url_slug(content_type, city_slug, lang)

    if not article_meta.get("title"):
        article_meta["title"] = f"{city_slug.replace('-', ' ').title()} Travel Guide 2026"
    if not article_meta.get("meta_description"):
        article_meta["meta_description"] = f"Complete travel guide to {city_slug.replace('-', ' ').title()} 2026. Hotels, attractions, flights, tips."

    seo = {
        "title": article_meta["title"],
        "meta_description": article_meta["meta_description"][:160],
        "h1": article_meta.get("h1", article_meta["title"]),
        "slug": slug,
        "canonical": f"/{lang}/{country_slug}/{slug}.html",
    }
    return seo


def build_breadcrumbs(country, city, content_type, lang):
    labels = {
        "ru": {"home": "Главная", "countries": "Страны"},
        "en": {"home": "Home", "countries": "Countries"},
    }
    l = labels.get(lang, labels["en"])

    breadcrumbs = [
        {"label": l["home"], "url": f"/{lang}/index.html"},
        {"label": l["countries"], "url": f"/{lang}/index.html"},
        {
            "label": country["name_en"] if lang == "en" else country["name_ru"],
            "url": f"/{lang}/{country['slug']}/index.html",
        },
    ]
    return breadcrumbs


def generate_schema_article(meta, city_name, country_name, url, lang):
    from datetime import date
    today = date.today().isoformat()
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta.get("h1", meta.get("title", "")),
        "description": meta.get("meta_description", ""),
        "author": {"@type": "Organization", "name": "TravelHub"},
        "datePublished": today,
        "dateModified": today,
        "publisher": {"@type": "Organization", "name": "TravelHub"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }


def generate_schema_breadcrumbs(breadcrumbs):
    items = []
    for i, bc in enumerate(breadcrumbs):
        items.append({
            "@type": "ListItem",
            "position": i + 1,
            "name": bc["label"],
            "item": bc["url"],
        })
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def generate_schema_faq(questions_answers):
    faq = []
    for q, a in questions_answers:
        faq.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq}


def generate_faq(city_name, content_type, lang, country_slug=None, city_slug=None):
    """Generate personalized FAQ based on city, country, and content type."""
    # Try to load country-specific FAQ data
    country_faq = {}
    if country_slug:
        try:
            from config.country_data import COUNTRY_DATA
            cd = COUNTRY_DATA.get(country_slug, {})
            if lang == "ru":
                country_faq = {q: a for q, a in cd.get("faq_ru", [])}
            else:
                country_faq = {q: a for q, a in cd.get("faq_en", [])}
        except ImportError:
            pass

    if lang == "ru":
        if content_type == "guide":
            faq = [
                ("Сколько дней нужно на осмотр {city}?".format(city=city_name),
                 "Для полноценного знакомства с {city} рекомендуем 4-7 дней. За это время можно осмотреть главные достопримечательности, попробовать местную кухню и отдохнуть.".format(city=city_name)),
                ("Какой бюджет нужен на поездку в {city}?".format(city=city_name),
                 "Средний бюджет на неделю в {city}: от $500 на человека без учёта перёта. Экономный вариант — от $300, комфортный — от $800.".format(city=city_name)),
                ("Когда лучше ехать в {city}?".format(city=city_name),
                 "Лучшее время для посещения {city} зависит от сезона. Смотрите наш гид по сезонам для подробной информации о погоде и ценах по месяцам.".format(city=city_name)),
                ("Безопасно ли в {city}?".format(city=city_name),
                 "{city} — популярное туристическое направление. При соблюдении стандартных мер предосторожности поездка безопасна.".format(city=city_name)),
            ]
            # Add visa FAQ from country data
            visa_q = "Нужна ли виза для поездки в {city}?".format(city=city_name)
            if country_faq:
                for q, a in country_faq.items():
                    if "виза" in q.lower() or "visa" in q.lower():
                        faq.insert(2, (visa_q, a))
                        break
                else:
                    faq.insert(2, (visa_q, "Гражданам РФ для посещения {city} требуется загранпаспорт. Подробности в разделе «Виза и документы».".format(city=city_name)))
            else:
                faq.insert(2, (visa_q, "Гражданам РФ для посещения {city} требуется загранпаспорт. Подробности в разделе «Виза и документы».".format(city=city_name)))

        elif content_type == "hotels":
            faq = [
                ("Сколько стоит отель в {city}?".format(city=city_name),
                 "Цены на отели в {city}: от $20-30 за_budgetный номер до $300+ за люкс. Средняя цена — $50-80 за номер среднего класса.".format(city=city_name)),
                ("Где лучше остановиться в {city}?".format(city=city_name),
                 "Выбор района зависит от цели поездки: центр — для экскурсий, побережье — для пляжного отдыха, окраины — для бюджетного варианта.".format(city=city_name)),
                ("Как забронировать отель дешевле?".format(city=city_name),
                 "Бронируйте за 2-3 месяца до поездки. Сравнивайте цены на Hotellook и Booking.com. В низкий сезон цены на 30-50% ниже.".format(city=city_name)),
            ]
        elif content_type == "flights":
            faq = [
                ("Сколько стоят билеты в {city}?".format(city=city_name),
                 "Средняя цена билета в {city}: от $200 в одну сторону. Билеты за 2-3 месяца до вылета дешевле на 20-40%.".format(city=city_name)),
                ("Есть ли прямые рейсы в {city}?".format(city=city_name),
                 "Наличие прямых рейсов зависит от города вылета. Проверяйте актуальные рейсы на Aviasales.".format(city=city_name)),
                ("Когда покупать билеты?".format(city=city_name),
                 "Оптимальное время покупки — за 2-3 месяца до вылета. Во время распродаж (вторник, среда) билеты дешевле.".format(city=city_name)),
            ]
        elif content_type == "attractions":
            faq = [
                ("Сколько стоят билеты в {city}?".format(city=city_name),
                 "Стоимость входа варьируется: от бесплатных достопримечательностей до $20-30 за музей. Многие площадки имеют льготные дни.".format(city=city_name)),
                ("Нужен ли гид в {city}?".format(city=city_name),
                 "Гид рекомендуется для исторических мест и сложных маршрутов. Самостоятельное путешествие возможно с помощью аудиогидов и карт.".format(city=city_name)),
            ]
        elif content_type == "seasons":
            faq = [
                ("Какая погода в {city}?".format(city=city_name),
                 "Погода в {city} меняется в зависимости от сезона. Смотрите подробную таблицу в статье.".format(city=city_name)),
                ("Когда самые низкие цены?".format(city=city_name),
                 "Низкий сезон — лучшее время для бюджетного отдыха. Цены на отели и билеты снижаются на 20-50%.".format(city=city_name)),
            ]
        else:
            faq = [
                ("Что важно знать о {city}?".format(city=city_name),
                 "Перед поездкой в {city} изучите информацию о погоде, документах и достопримечательностях.".format(city=city_name)),
            ]
    else:
        if content_type == "guide":
            faq = [
                (f"How many days do I need in {city_name}?",
                 f"For a full experience of {city_name}, we recommend 4-7 days. This covers major attractions, local cuisine, and relaxation."),
                (f"What's the budget for a trip to {city_name}?",
                 f"Average weekly budget: from $500 per person excluding flights. Budget option from $300, comfort from $800."),
                (f"When is the best time to visit {city_name}?",
                 f"Best time depends on the season — check our seasons guide for detailed weather and price information by month."),
                (f"Is {city_name} safe?",
                 f"{city_name} is a popular tourist destination. Travel is safe with standard precautions."),
            ]
            # Add visa FAQ from country data
            visa_q = f"Do I need a visa for {city_name}?"
            if country_faq:
                for q, a in country_faq.items():
                    if "visa" in q.lower():
                        faq.insert(2, (visa_q, a))
                        break
                else:
                    faq.insert(2, (visa_q, f"A passport is required for {city_name}. Check the visa section for details."))
            else:
                faq.insert(2, (visa_q, f"A passport is required for {city_name}. Check the visa section for details."))

        elif content_type == "hotels":
            faq = [
                (f"How much is a hotel in {city_name}?",
                 f"Hotel prices in {city_name}: from $20-30 for budget to $300+ for luxury. Average $50-80 for mid-range."),
                (f"Where is the best area to stay in {city_name}?",
                 f"Area choice depends on your purpose: center for sightseeing, beachfront for relaxation, outskirts for budget options."),
                (f"How to book a hotel cheaper?",
                 f"Book 2-3 months ahead. Compare prices on Hotellook and Booking.com. Low season prices are 30-50% lower."),
            ]
        elif content_type == "flights":
            faq = [
                (f"How much are flights to {city_name}?",
                 f"Average flight to {city_name}: from $200 one way. Tickets 2-3 months before departure are 20-40% cheaper."),
                (f"Are there direct flights to {city_name}?",
                 f"Direct flights depend on your departure city. Check current routes on Aviasales."),
                (f"When to buy tickets?",
                 f"Optimal time: 2-3 months before departure. Sales (Tuesday, Wednesday) offer cheaper tickets."),
            ]
        elif content_type == "attractions":
            faq = [
                (f"How much do attractions cost in {city_name}?",
                 f"Entrance fees vary: from free attractions to $20-30 for museums. Many venues have discount days."),
                (f"Do I need a guide in {city_name}?",
                 f"A guide is recommended for historical sites and complex routes. Self-guided travel is possible with audio guides and maps."),
            ]
        elif content_type == "seasons":
            faq = [
                (f"What's the weather like in {city_name}?",
                 f"Weather in {city_name} varies by season. See the detailed table in the article."),
                (f"When are prices lowest?",
                 f"Low season is the best time for budget travel. Hotel and flight prices drop 20-50%."),
            ]
        else:
            faq = [
                (f"What should I know about {city_name}?",
                 f"Before traveling to {city_name}, check weather, documents, and attractions."),
            ]

    return faq
