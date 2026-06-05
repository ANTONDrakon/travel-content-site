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


def build_seo_meta(article_meta, city_name, country_name, content_type, lang):
    slug = get_url_slug(content_type, city_name, lang)

    if not article_meta.get("title"):
        article_meta["title"] = f"{city_name} Travel Guide 2026"
    if not article_meta.get("meta_description"):
        article_meta["meta_description"] = f"Complete travel guide to {city_name} 2026. Hotels, attractions, flights, tips. Plan your trip to {city_name} today."

    seo = {
        "title": article_meta["title"],
        "meta_description": article_meta["meta_description"][:160],
        "h1": article_meta.get("h1", article_meta["title"]),
        "slug": slug,
        "canonical": f"/{lang}/{country_name}/{slug}.html",
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
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta.get("h1", meta.get("title", "")),
        "description": meta.get("meta_description", ""),
        "author": {"@type": "Organization", "name": "Travel Guide Hub"},
        "datePublished": "2026-01-15",
        "dateModified": "2026-06-01",
        "publisher": {"@type": "Organization", "name": "Travel Guide Hub"},
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


def generate_faq(city_name, content_type, lang):
    if lang == "ru":
        if content_type == "guide":
            return [
                ("Сколько дней нужно на осмотр {city}?".format(city=city_name),
                 "Для полноценного знакомства с {city} рекомендуем 4-7 дней.".format(city=city_name)),
                ("Какой бюджет нужен на поездку в {city}?".format(city=city_name),
                 "Средний бюджет на неделю: от $500 на человека без учёта перелёта."),
                ("Нужна ли виза для поездки в {city}?".format(city=city_name),
                 "Гражданам РФ для посещения {city} требуется загранпаспорт.".format(city=city_name)),
                ("Когда лучше ехать в {city}?".format(city=city_name),
                 "Лучшее время для посещения: зависит от сезона — смотрите наш гид по сезонам."),
                ("Безопасно ли в {city}?".format(city=city_name),
                 "{city} — популярное туристическое направление, безопасное при соблюдении стандартных мер.".format(city=city_name)),
            ]
        elif content_type == "hotels":
            return [
                ("Сколько стоит отель в {city}?".format(city=city_name),
                 "Цены на отели: от $20 за бюджетный номер до $300+ за люкс."),
                ("Где лучше остановиться в {city}?".format(city=city_name),
                 "Выбор района зависит от цели поездки: центр для экскурсий, побережье для пляжа."),
            ]
        else:
            return [
                ("Что важно знать о {city}?".format(city=city_name),
                 "Перед поездкой в {city} изучите информацию о погоде, документах и достопримечательностях.".format(city=city_name)),
            ]
    else:
        if content_type == "guide":
            return [
                (f"How many days do I need in {city_name}?",
                 f"For a full experience of {city_name}, we recommend 4-7 days."),
                (f"What's the budget for a trip to {city_name}?",
                 f"Average weekly budget: from $500 per person excluding flights."),
                (f"Do I need a visa for {city_name}?",
                 f"Visa requirements depend on your nationality — check with the local embassy."),
                (f"When is the best time to visit {city_name}?",
                 f"Best time depends on the season — check our seasons guide."),
                (f"Is {city_name} safe?",
                 f"{city_name} is a popular tourist destination, safe with standard precautions."),
            ]
        elif content_type == "hotels":
            return [
                (f"How much is a hotel in {city_name}?",
                 f"Hotel prices range from $20 for budget to $300+ for luxury."),
                (f"Where is the best area to stay in {city_name}?",
                 f"Area choice depends on your purpose: center for sightseeing, beachfront for relaxation."),
            ]
        else:
            return [
                (f"What should I know about {city_name}?",
                 f"Before traveling to {city_name}, check weather, documents, and attractions."),
            ]
