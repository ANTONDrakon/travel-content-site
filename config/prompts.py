CONTENT_TYPES = {
    "guide": {
        "slug": "guide",
        "category_ru": "Путеводители",
        "category_en": "Travel Guides",
        "priority": 1,
    },
    "hotels": {
        "slug": "hotels",
        "category_ru": "Отели",
        "category_en": "Hotels",
        "priority": 2,
    },
    "flights": {
        "slug": "flights",
        "category_ru": "Авиабилеты",
        "category_en": "Flights",
        "priority": 3,
    },
    "attractions": {
        "slug": "attractions",
        "category_ru": "Достопримечательности",
        "category_en": "Attractions",
        "priority": 4,
    },
    "seasons": {
        "slug": "seasons",
        "category_ru": "Сезоны и погода",
        "category_en": "Seasons & Weather",
        "priority": 5,
    },
}

PROMPTS = {
    "guide": {
        "ru": """Напиши статью-путеводитель: <article><h1>{city_name}: полный путеводитель 2026</h1>

Опиши город, атмосферу, почему стоит поехать (2-3 абзаца).

<h2>Как добраться</h2>
Аэропорты: {airports}. Рейсы из России, средняя цена билета. {flights_placeholder}

<h2>Где остановиться</h2>
Районы и отели для разного бюджета. {hotels_placeholder}

<h2>Топ-15 достопримечательностей</h2>
15 мест: название, описание (2-3 предложения), цена билета, часы работы.

<h2>Транспорт в городе</h2>
Метро, автобусы, такси, аренда. Цены.

<h2>Где поесть</h2>
Рестораны, уличная еда, местная кухня. Цены.

<h2>Лучшее время для поездки</h2>
Погода по месяцам, сезоны, цены.

<h2>Виза и документы</h2>
{visa_info}

<h2>Бюджет поездки на неделю</h2>
Проживание, еда, транспорт, развлечения — примерные суммы.

<h2>10 советов путешественникам</h2>
Практические советы для тех, кто едет впервые.</article>

Объём: 2000-3000 слов. Пиши полезно, с цифрами и фактами.""",

        "en": """Write a travel guide article: <article><h1>{city_name} Travel Guide 2026</h1>

Describe the city, atmosphere, why visit (2-3 paragraphs).

<h2>How to Get There</h2>
Airports: {airports}. Flights from major cities, average prices. {flights_placeholder}

<h2>Where to Stay</h2>
Neighborhoods and hotels for every budget. {hotels_placeholder}

<h2>Top 15 Attractions</h2>
15 places: name, description (2-3 sentences), ticket price, opening hours.

<h2>Getting Around</h2>
Metro, buses, taxis, rental. Prices.

<h2>Where to Eat</h2>
Restaurants, street food, local cuisine. Price ranges.

<h2>Best Time to Visit</h2>
Weather by month, seasons, prices.

<h2>Visa & Documents</h2>
{visa_info}

<h2>Weekly Trip Budget</h2>
Accommodation, food, transport, entertainment — approximate costs.

<h2>10 Travel Tips</h2>
Practical tips for first-time visitors.</article>

Length: 2000-3000 words. Be useful, with numbers and facts."""
    },

    "hotels": {
        "ru": """Напиши статью: <article><h1>Топ-10 отелей в {city_name} 2026: от бюджета до люкса</h1>

О гостиничной инфраструктуре, районах, ценах (2 абзаца).

<h2>Бюджетные отели (до $50/ночь)</h2>
3 отеля: название, описание, цены, плюсы/минусы. {hotels_placeholder}

<h2>Отели среднего класса ($50-150/ночь)</h2>
4 отеля: название, описание, цены, фишки. {hotels_placeholder}

<h2>Люксовые отели (от $150/ночь)</h2>
3 отеля: название, описание, особенности. {hotels_placeholder}

<h2>Как выбрать район</h2>
По целям поездки: пляж, экскурсии, ночная жизнь.

<h2>Советы по бронированию</h2>
Как сэкономить, когда бронировать, лучшие сервисы. {hotels_placeholder}</article>

1500-2500 слов.""",

        "en": """Write an article: <article><h1>Top 10 Hotels in {city_name} 2026: Budget to Luxury</h1>

Hotel infrastructure, neighborhoods, prices (2 paragraphs).

<h2>Budget Hotels (under $50/night)</h2>
3 hotels: name, description, prices, pros/cons. {hotels_placeholder}

<h2>Mid-Range Hotels ($50-150/night)</h2>
4 hotels: name, description, prices, highlights. {hotels_placeholder}

<h2>Luxury Hotels ($150+/night)</h2>
3 hotels: name, description, features. {hotels_placeholder}

<h2>How to Choose the Right Area</h2>
By purpose: beach, sightseeing, nightlife.

<h2>Booking Tips</h2>
How to save, when to book, best services. {hotels_placeholder}</article>

1500-2500 words."""
    },

    "flights": {
        "ru": """Напиши статью: <article><h1>Как дёшево добраться до {city_name} в 2026</h1>

Аэропорты {city_name}: {airports}. Авиакомпании по направлению.

<h2>Прямые рейсы из России</h2>
Авиакомпании, города вылета, примерные цены. {flights_placeholder}

<h2>Рейсы с пересадками</h2>
Самые дешёвые варианты, через какие города, длительность.

<h2>Цены по месяцам</h2>
Таблица средних цен в 2026: январь-декабрь.

<h2>10 лайфхаков для дешёвых билетов</h2>
Конкретные советы с сервисами. {flights_placeholder}

<h2>Когда покупать билеты</h2>
Оптимальные сроки до вылета.</article>

1500-2000 слов.""",

        "en": """Write an article: <article><h1>How to Find Cheap Flights to {city_name} 2026</h1>

{city_name} airports: {airports}. Airlines serving the route.

<h2>Direct Flights</h2>
Airlines, departure cities, estimated prices. {flights_placeholder}

<h2>Connecting Flights</h2>
Cheapest options, via which cities, duration.

<h2>Prices by Month</h2>
Table of average 2026 prices: January-December.

<h2>10 Hacks for Cheap Flights</h2>
Specific tips with services. {flights_placeholder}

<h2>When to Book</h2>
Optimal timing before departure.</article>

1500-2000 words."""
    },

    "attractions": {
        "ru": """Напиши статью: <article><h1>Что посмотреть в {city_name}: 15 лучших мест 2026</h1>

Почему {city_name} стоит посетить ради достопримечательностей.

<h2>15 лучших достопримечательностей</h2>
По каждому месту: название, описание (3-4 предложения), цена билета, часы работы, как добраться, совет.

<h2>Маршруты на 1, 2 и 3 дня</h2>
Оптимальные маршруты по городу.

<h2>Экскурсии и туры</h2>
Какие экскурсии стоит взять, цены. {tours_placeholder}

<h2>Бесплатные достопримечательности</h2>
Что можно посмотреть без билетов.

<h2>Практические советы</h2>
Транспорт до достопримечательностей, комбо-билеты. {hotels_placeholder}</article>

2000-2500 слов.""",

        "en": """Write an article: <article><h1>15 Best Things to Do in {city_name} 2026</h1>

Why visit {city_name} for its attractions.

<h2>15 Best Attractions</h2>
Each: name, description (3-4 sentences), ticket price, hours, how to get there, tip.

<h2>1-Day, 2-Day, 3-Day Itineraries</h2>
Optimal city routes.

<h2>Tours & Excursions</h2>
Which tours to take, prices. {tours_placeholder}

<h2>Free Attractions</h2>
What to see without tickets.

<h2>Practical Tips</h2>
Transportation, combo tickets. {hotels_placeholder}</article>

2000-2500 words."""
    },

    "seasons": {
        "ru": """Напиши статью: <article><h1>Когда лучше ехать в {city_name}: сезоны, погода и цены 2026</h1>

Общая информация о климате.

<h2>Погода по месяцам</h2>
Таблица: температура воздуха, воды, осадки, солнечные дни — январь-декабрь.

<h2>Высокий сезон</h2>
Когда, почему, цены. {hotels_placeholder}

<h2>Низкий сезон</h2>
Когда, плюсы/минусы, погода, цены.

<h2>Лучшее время для пляжного отдыха</h2>
Оптимальные месяцы для купания.

<h2>Лучшее время для экскурсий</h2>
Когда комфортнее осматривать город.

<h2>Сезон дождей</h2>
Когда, насколько сильные, стоит ли ехать.

<h2>События и фестивали</h2>
Главные события по месяцам.

<h2>Вывод</h2>
Лучшие месяцы — резюме. {flights_placeholder}</article>

1500-2000 слов.""",

        "en": """Write an article: <article><h1>Best Time to Visit {city_name} 2026: Seasons & Weather</h1>

General climate information.

<h2>Weather by Month</h2>
Table: air temp, water temp, precipitation, sunny days — January-December.

<h2>High Season</h2>
When, why, prices. {hotels_placeholder}

<h2>Low Season</h2>
When, pros/cons, weather, prices.

<h2>Best Time for Beach Vacation</h2>
Optimal months for swimming.

<h2>Best Time for Sightseeing</h2>
Most comfortable months.

<h2>Rainy Season</h2>
When, intensity, worth visiting?

<h2>Events & Festivals</h2>
Major events by month.

<h2>Conclusion</h2>
Best months — summary. {flights_placeholder}</article>

1500-2000 words."""
    },
}
