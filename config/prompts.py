CONTENT_TYPES = {
    "guide": {
        "slug": "guide",
        "category_ru": "Путеводители",
        "category_en": "Travel Guides",
        "category_es": "Guías de Viaje",
        "priority": 1,
    },
    "hotels": {
        "slug": "hotels",
        "category_ru": "Отели",
        "category_en": "Hotels",
        "category_es": "Hoteles",
        "priority": 2,
    },
    "flights": {
        "slug": "flights",
        "category_ru": "Авиабилеты",
        "category_en": "Flights",
        "category_es": "Vuelos",
        "priority": 3,
    },
    "attractions": {
        "slug": "attractions",
        "category_ru": "Достопримечательности",
        "category_en": "Attractions",
        "category_es": "Atracciones",
        "priority": 4,
    },
    "seasons": {
        "slug": "seasons",
        "category_ru": "Сезоны и погода",
        "category_en": "Seasons & Weather",
        "category_es": "Temporadas y Clima",
        "priority": 5,
    },
}

PROMPTS = {
    "guide": {
        "ru": """Напиши статью-путеводитель: <article><h1>{city_name}: полный путеводитель 2026</h1>

Опиши город, атмосферу, почему стоит поехать (2-3 абзаца).

<h2>Как добраться</h2>
Аэропорты: {airports}. Рейсы из России, средняя цена билета. В конце абзаца естественно упомяни, что билеты можно {flights_placeholder}.

<h2>Где остановиться</h2>
Районы и отели для разного бюджета. В тексте естественно упомяни, что цены на отели в городе можно {hotels_placeholder}.

<h2>Топ-15 достопримечательностей</h2>
15 мест: название, описание (2-3 предложения), цена билета, часы работы.

<h2>Транспорт в городе</h2>
Метро, автобусы, такси, аренда. Цены.

<h2>Где поесть</h2>
Рестораны, уличная еда, местная кухня. Цены.

<h2>Экскурсии и туры</h2>
Лучшие экскурсии, цены, что посмотреть. Упомяни что подходящие экскурсии можно {excursions_placeholder}.

<h2>Трансфер из аэропорта</h2>
Как добраться из аэропорта: такси, трансфер, общественный транспорт. Упомяни что удобный трансфер можно {transfers_placeholder}.

<h2>Связь и интернет</h2>
Wi-Fi, местная SIM-карта, eSIM. Упомяни что eSIM для поездки можно {esim_placeholder}.

<h2>Лучшее время для поездки</h2>
Погода по месяцам, сезоны, цены.

<h2>Виза и документы</h2>
{visa_info}

<h2>Валюта и деньги</h2>
Местная валюта: {currency_info}. Где обменять, можно ли платить картой, сколько наличных брать.

<h2>Часовой пояс</h2>
{timezone_info}. Разница с Москвой.

<h2>Бюджет поездки на неделю</h2>
Проживание, еда, транспорт, развлечения — примерные суммы в местной валюте.

<h2>Страхование</h2>
Обязательно ли, что покрывает, сколько стоит. Оформить страховку можно {insurance_placeholder}.

<h2>10 советов путешественникам</h2>
Практические советы для тех, кто едет впервые.</article>

Объём: 2000-3000 слов. Пиши полезно, с цифрами и фактами. Встраивай ссылки естественно как часть предложений, не как отдельные блоки.""",

        "en": """Write a travel guide article: <article><h1>{city_name} Travel Guide 2026</h1>

Describe the city, atmosphere, why visit (2-3 paragraphs).

<h2>How to Get There</h2>
Airports: {airports}. Flights from major cities, average prices. Naturally mention that flights can be {flights_placeholder} at the end of the paragraph.

<h2>Where to Stay</h2>
Neighborhoods and hotels for every budget. Naturally mention that hotel prices can be {hotels_placeholder} in the text.

<h2>Top 15 Attractions</h2>
15 places: name, description (2-3 sentences), ticket price, opening hours.

<h2>Getting Around</h2>
Metro, buses, taxis, rental. Prices.

<h2>Where to Eat</h2>
Restaurants, street food, local cuisine. Price ranges.

<h2>Tours & Excursions</h2>
Best excursions, prices, what to see. Mention that tours can be {excursions_placeholder}.

<h2>Airport Transfer</h2>
How to get from the airport: taxi, transfer, public transport. Mention that a convenient transfer can be {transfers_placeholder}.

<h2>Connectivity</h2>
Wi-Fi, local SIM, eSIM. Mention that an eSIM for the trip can be {esim_placeholder}.

<h2>Best Time to Visit</h2>
Weather by month, seasons, prices.

<h2>Visa & Documents</h2>
{visa_info}

<h2>Currency & Money</h2>
Local currency: {currency_info}. Where to exchange, can you pay by card, how much cash to bring.

<h2>Time Zone</h2>
{timezone_info}. Difference from major hubs.

<h2>Weekly Trip Budget</h2>
Accommodation, food, transport, entertainment — approximate costs in local currency.

<h2>Travel Insurance</h2>
Is it mandatory, what it covers, how much it costs. Get insurance via {insurance_placeholder}.

<h2>10 Travel Tips</h2>
Practical tips for first-time visitors.</article>

Length: 2000-3000 words. Be useful, with numbers and facts. Weave affiliate links naturally into sentences, not as separate blocks.""",

        "es": """Escribe un artículo guía de viaje: <article><h1>Guía de viaje de {city_name} 2026</h1>

Describe la ciudad, la atmósfera, por qué visitar (2-3 párrafos).

<h2>Cómo Llegar</h2>
Aeropuertos: {airports}. Vuelos desde ciudades principales, precios promedio. Menciona naturalmente que los vuelos se pueden {flights_placeholder} al final del párrafo.

<h2>Dónde Alojarse</h2>
Barrios y hoteles para todos los presupuestos. Menciona naturalmente que los precios de hoteles se pueden {hotels_placeholder} en el texto.

<h2>Top 15 Atracciones</h2>
15 lugares: nombre, descripción (2-3 oraciones), precio de entrada, horarios.

<h2>Cómo Movilizarse</h2>
Metro, autobuses, taxis, alquiler. Precios.

<h2>Dónde Comer</h2>
Restaurantes, comida callejera, cocina local. Rangos de precios.

<h2>Tours y Excursiones</h2>
Mejores excursiones, precios, qué ver. Menciona que los tours se pueden {excursions_placeholder}.

<h2>Transfer desde el Aeropuerto</h2>
Cómo llegar desde el aeropuerto: taxi, transfer, transporte público. Menciona que un transfer conveniente se puede {transfers_placeholder}.

<h2>Conectividad</h2>
Wi-Fi, SIM local, eSIM. Menciona que una eSIM para el viaje se puede {esim_placeholder}.

<h2>Mejor Época para Visitar</h2>
Clima por mes, temporadas, precios.

<h2>Visa y Documentos</h2>
{visa_info}

<h2>Moneda y Dinero</h2>
Moneda local: {currency_info}. Dónde cambiar, se puede pagar con tarjeta, cuánto efectivo llevar.

<h2>Zona Horaria</h2>
{timezone_info}. Diferencia con los principales hubs.

<h2>Presupuesto Semanal de Viaje</h2>
Alojamiento, comida, transporte, entretenimiento — costos aproximados en moneda local.

<h2>Seguro de Viaje</h2>
¿Es obligatorio, qué cubre, cuánto cuesta? Contrata seguro vía {insurance_placeholder}.

<h2>10 Consejos para Viajeros</h2>
Consejos prácticos para visitantes por primera vez.</article>

Longitud: 2000-3000 palabras. Sé útil, con números y datos. Integra los enlaces de afiliados de forma natural en las oraciones, no como bloques separados."""
    },

    "hotels": {
        "ru": """Напиши статью: <article><h1>Топ-10 отелей в {city_name} 2026: от бюджета до люкса</h1>

О гостиничной инфраструктуре, районах, ценах (2 абзаца). В конце введения естественно упомяни что цены на отели в {city_name} можно {hotels_placeholder}.

<h2>Бюджетные отели (до $50/ночь)</h2>
3 отеля: название, описание, цены, плюсы/минусы.

<h2>Отели среднего класса ($50-150/ночь)</h2>
4 отеля: название, описание, цены, фишки.

<h2>Люксовые отели (от $150/ночь)</h2>
3 отеля: название, описание, особенности.

<h2>Как выбрать район</h2>
По целям поездки: пляж, экскурсии, ночная жизнь.

<h2>Как добраться из аэропорта</h2>
Трансферы до отелей. Упомяни что удобный трансфер можно {transfers_placeholder}.

<h2>Советы по бронированию</h2>
Как сэкономить, когда бронировать, лучшие сервисы. Упомяни что на многих площадках можно {hotels_placeholder} и сравнить цены.</article>

1500-2500 слов.""",

        "en": """Write an article: <article><h1>Top 10 Hotels in {city_name} 2026: Budget to Luxury</h1>

Hotel infrastructure, neighborhoods, prices (2 paragraphs). Naturally mention that hotel prices in {city_name} can be {hotels_placeholder} at the end of the intro.

<h2>Budget Hotels (under $50/night)</h2>
3 hotels: name, description, prices, pros/cons.

<h2>Mid-Range Hotels ($50-150/night)</h2>
4 hotels: name, description, prices, highlights.

<h2>Luxury Hotels ($150+/night)</h2>
3 hotels: name, description, features.

<h2>How to Choose the Right Area</h2>
By purpose: beach, sightseeing, nightlife.

<h2>Airport Transfers</h2>
Getting to hotels from the airport. Mention that a convenient transfer can be {transfers_placeholder}.

<h2>Booking Tips</h2>
How to save, when to book, best services. Mention that you can {hotels_placeholder} to compare prices.</article>

1500-2500 words.""",

        "es": """Escribe un artículo: <article><h1>Top 10 Hoteles en {city_name} 2026: De Económico a Lujo</h1>

Infraestructura hotelera, barrios, precios (2 párrafos). Menciona naturalmente que los precios de hoteles en {city_name} se pueden {hotels_placeholder} al final de la introducción.

<h2>Hoteles Económicos (menos de $50/noche)</h2>
3 hoteles: nombre, descripción, precios, pros/contras.

<h2>Hoteles de Gama Media ($50-150/noche)</h2>
4 hoteles: nombre, descripción, precios, aspectos destacados.

<h2>Hoteles de Lujo ($150+/noche)</h2>
3 hoteles: nombre, descripción, características.

<h2>Cómo Elegir el Barrio Correcto</h2>
Según el propósito: playa, turismo, vida nocturna.

<h2>Transfers desde el Aeropuerto</h2>
Cómo llegar a los hoteles desde el aeropuerto. Menciona que un transfer conveniente se puede {transfers_placeholder}.

<h2>Consejos de Reserva</h2>
Cómo ahorrar, cuándo reservar, mejores servicios. Menciona que puedes {hotels_placeholder} para comparar precios.</article>

1500-2500 palabras."""
    },

    "flights": {
        "ru": """Напиши статью: <article><h1>Как дёшево добраться до {city_name} в 2026</h1>

Аэропорты {city_name}: {airports}. Авиакомпании по направлению.

<h2>Прямые рейсы из России</h2>
Авиакомпании, города вылета, примерные цены.

<h2>Рейсы с пересадками</h2>
Самые дешёвые варианты, через какие города, длительность. Упомяни что билеты можно {flights_placeholder} и сравнить цены по разным датам.

<h2>Цены по месяцам</h2>
Таблица средних цен в 2026: январь-декабрь.

<h2>10 лайфхаков для дешёвых билетов</h2>
Конкретные советы с сервисами.

<h2>Когда покупать билеты</h2>
Оптимальные сроки до вылета.

<h2>Страхование полёта</h2>
Что делать при задержке или отмене рейса. Упомяни что компенсацию можно получить через {insurance_placeholder}.</article>

1500-2000 слов.""",

        "en": """Write an article: <article><h1>How to Find Cheap Flights to {city_name} 2026</h1>

{city_name} airports: {airports}. Airlines serving the route.

<h2>Direct Flights</h2>
Airlines, departure cities, estimated prices.

<h2>Connecting Flights</h2>
Cheapest options, via which cities, duration. Mention that flights can be {flights_placeholder} and prices compared across dates.

<h2>Prices by Month</h2>
Table of average 2026 prices: January-December.

<h2>10 Hacks for Cheap Flights</h2>
Specific tips with services.

<h2>When to Book</h2>
Optimal timing before departure.

<h2>Flight Insurance</h2>
What to do if your flight is delayed or cancelled. Mention compensation via {insurance_placeholder}.</article>

1500-2000 words.""",

        "es": """Escribe un artículo: <article><h1>Cómo Encontrar Vuelos Baratos a {city_name} 2026</h1>

Aeropuertos de {city_name}: {airports}. Aerolíneas que cubren la ruta.

<h2>Vuelos Directos</h2>
Aerolíneas, ciudades de salida, precios estimados.

<h2>Vuelos con Escala</h2>
Opciones más baratas, a través de qué ciudades, duración. Menciona que los vuelos se pueden {flights_placeholder} y comparar precios entre fechas.

<h2>Precios por Mes</h2>
Tabla de precios promedio 2026: enero-diciembre.

<h2>10 Trucos para Vuelos Baratos</h2>
Consejos específicos con servicios.

<h2>Cuándo Comprar</h2>
Momento óptimo antes de la salida.

<h2>Seguro de Vuelo</h2>
Qué hacer si tu vuelo se retrasa o cancela. Menciona compensación vía {insurance_placeholder}.</article>

1500-2000 palabras."""
    },

    "attractions": {
        "ru": """Напиши статью: <article><h1>Что посмотреть в {city_name}: 15 лучших мест 2026</h1>

Почему {city_name} стоит посетить ради достопримечательностей.

<h2>15 лучших достопримечательностей</h2>
По каждому месту: название, описание (3-4 предложения), цена билета, часы работы, как добраться, совет.

<h2>Маршруты на 1, 2 и 3 дня</h2>
Оптимальные маршруты по городу.

<h2>Экскурсии и туры</h2>
Какие экскурсии стоит взять, цены. Упомяни что подходящие экскурсии можно {excursions_placeholder}.

<h2>Билеты онлайн</h2>
Где покупать билеты дешевле. Упомяни что билеты на достопримечательности можно {tickets_placeholder}.

<h2>Бесплатные достопримечательности</h2>
Что можно посмотреть без билетов.

<h2>Практические советы</h2>
Транспорт до достопримечательностей, комбо-билеты.</article>

2000-2500 слов.""",

        "en": """Write an article: <article><h1>15 Best Things to Do in {city_name} 2026</h1>

Why visit {city_name} for its attractions.

<h2>15 Best Attractions</h2>
Each: name, description (3-4 sentences), ticket price, hours, how to get there, tip.

<h2>1-Day, 2-Day, 3-Day Itineraries</h2>
Optimal city routes.

<h2>Tours & Excursions</h2>
Which tours to take, prices. Mention that tours can be {excursions_placeholder}.

<h2>Book Tickets Online</h2>
Where to buy tickets cheaper. Mention that attraction tickets can be {tickets_placeholder}.

<h2>Free Attractions</h2>
What to see without tickets.

<h2>Practical Tips</h2>
Transportation, combo tickets.</article>

2000-2500 words.""",

        "es": """Escribe un artículo: <article><h1>15 Mejores Cosas para Hacer en {city_name} 2026</h1>

Por qué visitar {city_name} por sus atracciones.

<h2>15 Mejores Atracciones</h2>
Cada una: nombre, descripción (3-4 oraciones), precio de entrada, horarios, cómo llegar, consejo.

<h2>Itinerarios de 1, 2 y 3 Días</h2>
Rutas óptimas por la ciudad.

<h2>Tours y Excursiones</h2>
Qué tours tomar, precios. Menciona que los tours se pueden {excursions_placeholder}.

<h2>Reserva Entradas Online</h2>
Dónde comprar entradas más baratas. Menciona que las entradas a atracciones se pueden {tickets_placeholder}.

<h2>Atracciones Gratuitas</h2>
Qué ver sin entradas.

<h2>Consejos Prácticos</h2>
Transporte, entradas combinadas.</article>

2000-2500 palabras."""
    },

    "seasons": {
        "ru": """Напиши статью: <article><h1>Когда лучше ехать в {city_name}: сезоны, погода и цены 2026</h1>

Общая информация о климате.

<h2>Погода по месяцам</h2>
Таблица: температура воздуха, воды, осадки, солнечные дни — январь-декабрь.

<h2>Высокий сезон</h2>
Когда, почему, цены. Упомяни что в высокий сезон стоит заранее {hotels_placeholder}.

<h2>Низкий сезон</h2>
Когда, плюсы/минусы, погода, цены.

<h2>Лучшее время для пляжного отдыха</h2>
Оптимальные месяцы для купания.

<h2>Лучшее время для экскурсий</h2>
Когда комфортнее осматривать город. Экскурсии можно {excursions_placeholder}.

<h2>Сезон дождей</h2>
Когда, насколько сильные, стоит ли ехать.

<h2>События и фестивали</h2>
Главные события по месяцам.

<h2>Вывод</h2>
Лучшие месяцы — резюме. Билеты на эти даты можно {flights_placeholder}.</article>

1500-2000 слов.""",

        "en": """Write an article: <article><h1>Best Time to Visit {city_name} 2026: Seasons & Weather</h1>

General climate information.

<h2>Weather by Month</h2>
Table: air temp, water temp, precipitation, sunny days — January-December.

<h2>High Season</h2>
When, why, prices. Mention that during high season it's worth booking hotels early via {hotels_placeholder}.

<h2>Low Season</h2>
When, pros/cons, weather, prices.

<h2>Best Time for Beach Vacation</h2>
Optimal months for swimming.

<h2>Best Time for Sightseeing</h2>
Most comfortable months. Excursions can be {excursions_placeholder}.

<h2>Rainy Season</h2>
When, intensity, worth visiting?

<h2>Events & Festivals</h2>
Major events by month.

<h2>Conclusion</h2>
Best months — summary. Flights for those dates can be {flights_placeholder}.</article>

1500-2000 words.""",

        "es": """Escribe un artículo: <article><h1>Mejor Época para Visitar {city_name} 2026: Temporadas y Clima</h1>

Información general sobre el clima.

<h2>Clima por Mes</h2>
Tabla: temperatura del aire, del agua, precipitación, días soleados — enero a diciembre.

<h2>Alta Temporada</h2>
Cuándo, por qué, precios. Menciona que en alta temporada vale la pena reservar hoteles pronto vía {hotels_placeholder}.

<h2>Baja Temporada</h2>
Cuándo, pros/contras, clima, precios.

<h2>Mejor Época para Vacaciones de Playa</h2>
Meses óptimos para nadar.

<h2>Mejor Época para Turismo</h2>
Meses más cómodos. Excursiones se pueden {excursions_placeholder}.

<h2>Temporada de Lluvias</h2>
Cuándo, intensidad, ¿vale la pena visitar?

<h2>Eventos y Festivales</h2>
Principales eventos por mes.

<h2>Conclusión</h2>
Mejores meses — resumen. Vuelos para esas fechas se pueden {flights_placeholder}.</article>

1500-2000 palabras."""
    },
}
