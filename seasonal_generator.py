"""
Seasonal Pages Generator for TravelHub
Generates "Where to go in [Month]" pages with destination recommendations.
"""
import os
from pathlib import Path
from datetime import date

OUTPUT_DIR = Path(__file__).parent / "docs"
SITE_URL = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")
CONTENT_DIR = Path(__file__).parent / "content"

# Month data in both languages
MONTHS = {
    "january": {"ru": "январь", "en": "January", "emoji": "❄️"},
    "february": {"ru": "февраль", "en": "February", "emoji": "❄️"},
    "march": {"ru": "март", "en": "March", "emoji": "🌸"},
    "april": {"ru": "апрель", "en": "April", "emoji": "🌸"},
    "may": {"ru": "май", "en": "May", "emoji": "☀️"},
    "june": {"ru": "июнь", "en": "June", "emoji": "☀️"},
    "july": {"ru": "июль", "en": "July", "emoji": "🔥"},
    "august": {"ru": "август", "en": "August", "emoji": "🔥"},
    "september": {"ru": "сентябрь", "en": "September", "emoji": "🍂"},
    "october": {"ru": "октябрь", "en": "October", "emoji": "🍂"},
    "november": {"ru": "ноябрь", "en": "November", "emoji": "🌧"},
    "december": {"ru": "декабрь", "en": "December", "emoji": "❄️"},
}

# Seasonal recommendations for each month
SEASONAL_DATA = {
    "january": {
        "hero_image": "https://images.unsplash.com/photo-1548263594-a71f2df4da24?w=1600&q=80",
        "destinations": [
            {"slug": "thailand", "temp": "+28-32°C", "budget_ru": "₽90 000", "budget_en": "$900", "highlights_ru": ["Пляжи", "Массаж"], "highlights_en": ["Beaches", "Spa"],
             "description_ru": "Высокий сезон. Идеальная погода, сухо, тепло. Лучшее время для пляжного отдыха.",
             "description_en": "Peak season. Perfect weather, dry and warm. Best time for beach vacation."},
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽250 000", "budget_en": "$2 500", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Сухой сезон. Кристально чистое море, идеальные условия для дайвинга.",
             "description_en": "Dry season. Crystal clear sea, perfect diving conditions."},
            {"slug": "uae", "temp": "+22-25°C", "budget_ru": "₽80 000", "budget_en": "$800", "highlights_ru": ["Шопинг", "Экскурсии"], "highlights_en": ["Shopping", "Sightseeing"],
             "description_ru": "Идеальная погода для экскурсий. Не жарко, комфортно для прогулок.",
             "description_en": "Perfect weather for sightseeing. Not hot, comfortable for walking."},
            {"slug": "georgia", "temp": "+2-8°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Горы", "Кухня"], "highlights_en": ["Mountains", "Food"],
             "description_ru": "Зимний отдых: горные лыжи в Гудаури, грузинская кухня, горячие источники.",
             "description_en": "Winter vacation: skiing in Gudauri, Georgian cuisine, hot springs."},
            {"slug": "sri-lanka", "temp": "+26-29°C", "budget_ru": "₽50 000", "budget_en": "$500", "highlights_ru": ["Пляжи", "Храмы"], "highlights_en": ["Beaches", "Temples"],
             "description_ru": "Сухой сезон на западном побережье. Идеально для пляжей и экскурсий.",
             "description_en": "Dry season on the west coast. Perfect for beaches and sightseeing."},
        ],
        "tips_ru": """
<h2>Куда поехать в январе</h2>
<p>Январь — отличный месяц для путешествий. Зима в Европе и России, но в Азии и на Ближнем Востоке — идеальная погода.</p>

<h2>Топ-5 направлений</h2>
<ul>
<li><strong>Таиланд</strong> — высокий сезон, +28-32°C, сухо. Идеально для пляжей.</li>
<li><strong>Мальдивы</strong> — сухой сезон, кристальное море. Для романтических поездок.</li>
<li><strong>ОАЭ</strong> — комфортные +22-25°C, шопинг и экскурсии.</li>
<li><strong>Грузия</strong> — горные лыжи в Гудаури, грузинская кухня.</li>
<li><strong>Шри-Ланка</strong> — пляжи и храмы, бюджетный отдых.</li>
</ul>

<h2>Советы</h2>
<ul>
<li>Бронируйте за 2-3 месяца до поездки — цены ниже.</li>
<li>В Таиланд и Мальдивы берите солнцезащитный крем с высоким SPF.</li>
<li>В Грузию — тёплую одежду для гор.</li>
</ul>
""",
        "tips_en": """
<h2>Where to Go in January</h2>
<p>January is great for travel. Winter in Europe and Russia, but perfect weather in Asia and the Middle East.</p>

<h2>Top 5 Destinations</h2>
<ul>
<li><strong>Thailand</strong> — peak season, +28-32°C, dry. Perfect for beaches.</li>
<li><strong>Maldives</strong> — dry season, crystal clear sea. For romantic trips.</li>
<li><strong>UAE</strong> — comfortable +22-25°C, shopping and sightseeing.</li>
<li><strong>Georgia</strong> — skiing in Gudauri, Georgian cuisine.</li>
<li><strong>Sri Lanka</strong> — beaches and temples, budget vacation.</li>
</ul>

<h2>Tips</h2>
<ul>
<li>Book 2-3 months ahead for better prices.</li>
<li>Bring high SPF sunscreen for Thailand and Maldives.</li>
<li>Bring warm clothes for Georgia mountains.</li>
</ul>
""",
    },
    "february": {
        "hero_image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80",
        "destinations": [
            {"slug": "thailand", "temp": "+28-32°C", "budget_ru": "₽90 000", "budget_en": "$900", "highlights_ru": ["Пляжи", "Фестивали"], "highlights_en": ["Beaches", "Festivals"],
             "description_ru": "Продолжение высокого сезона. Тепло, сухо, идеально для отдыха.",
             "description_en": "Continuation of peak season. Warm, dry, perfect for vacation."},
            {"slug": "egypt", "temp": "+20-25°C", "budget_ru": "₽60 000", "budget_en": "$600", "highlights_ru": ["Дайвинг", "Экскурсии"], "highlights_en": ["Diving", "Excursions"],
             "description_ru": "Комфортная погода для экскурсий к пирамидам и дайвинга в Красном море.",
             "description_en": "Comfortable weather for pyramid excursions and Red Sea diving."},
            {"slug": "indonesia", "temp": "+27-30°C", "budget_ru": "₽80 000", "budget_en": "$800", "highlights_ru": ["Сёрфинг", "Йога"], "highlights_en": ["Surf", "Yoga"],
             "description_ru": "Влажный сезон, но короткие ливни. Меньше туристов, ниже цены.",
             "description_en": "Wet season, but short showers. Fewer tourists, lower prices."},
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽250 000", "budget_en": "$2 500", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Сухой сезон продолжается. Идеально для медового месяца.",
             "description_en": "Dry season continues. Perfect for honeymoon."},
        ],
        "tips_ru": """
<h2>Куда поехать в феврале</h2>
<p>Февраль — последний месяц зимы. Отличное время для тёплых направлений.</p>

<h2>Топ-5 направлений</h2>
<ul>
<li><strong>Таиланд</strong> — высокий сезон, идеальная погода.</li>
<li><strong>Египет</strong> — комфортные +20-25°C, дайвинг.</li>
<li><strong>Индонезия</strong> — бюджетный отдых на Бали.</li>
<li><strong>Мальдивы</strong> — романтика и дайвинг.</li>
<li><strong>ОАЭ</strong> — шопинг и развлечения.</li>
</ul>
""",
        "tips_en": """
<h2>Where to Go in February</h2>
<p>February is the last month of winter. Great time for warm destinations.</p>

<h2>Top 5 Destinations</h2>
<ul>
<li><strong>Thailand</strong> — peak season, perfect weather.</li>
<li><strong>Egypt</strong> — comfortable +20-25°C, diving.</li>
<li><strong>Indonesia</strong> — budget vacation in Bali.</li>
<li><strong>Maldives</strong> — romance and diving.</li>
<li><strong>UAE</strong> — shopping and entertainment.</li>
</ul>
""",
    },
    "march": {
        "hero_image": "https://images.unsplash.com/photo-1462275646964-a0e3c11f18a6?w=1600&q=80",
        "destinations": [
            {"slug": "turkey", "temp": "+15-20°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Тюльпаны", "Экскурсии"], "highlights_en": ["Tulips", "Sightseeing"],
             "description_ru": "Цветение тюльпанов в Стамбуле. Идеальная погода для экскурсий.",
             "description_en": "Tulip bloom in Istanbul. Perfect weather for sightseeing."},
            {"slug": "thailand", "temp": "+30-35°C", "budget_ru": "₽90 000", "budget_en": "$900", "highlights_ru": ["Пляжи", "Фестивали"], "highlights_en": ["Beaches", "Festivals"],
             "description_ru": "Жаркий сезон. Сонгкран в апреле — тайский Новый год.",
             "description_en": "Hot season. Songkran in April — Thai New Year."},
            {"slug": "georgia", "temp": "+8-14°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Горы", "Весна"], "highlights_en": ["Mountains", "Spring"],
             "description_ru": "Ранняя весна. Цветение, мало туристов, бюджетный отдых.",
             "description_en": "Early spring. Blooming, few tourists, budget vacation."},
            {"slug": "vietnam", "temp": "+25-30°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Пляжи", "Еда"], "highlights_en": ["Beaches", "Food"],
             "description_ru": "Сухой сезон на юге. Идеально для Фукуока и Дананга.",
             "description_en": "Dry season in the south. Perfect for Phu Quoc and Da Nang."},
        ],
        "tips_ru": """
<h2>Куда поехать в марте</h2>
<p>Март — начало весны. Отличное время для путешествий в Азию и на Кавказ.</p>
<h2>Топ направления</h2>
<ul>
<li><strong>Турция</strong> — цветение тюльпанов, экскурсии.</li>
<li><strong>Таиланд</strong> — жаркий сезон, готовьтесь к Сонгкрану.</li>
<li><strong>Грузия</strong> — ранняя весна, горы.</li>
<li><strong>Вьетнам</strong> — пляжи юга.</li>
</ul>
""",
        "tips_en": """
<h2>Where to Go in March</h2>
<p>March is the start of spring. Great time for Asia and Caucasus.</p>
<h2>Top Destinations</h2>
<ul>
<li><strong>Turkey</strong> — tulip bloom, sightseeing.</li>
<li><strong>Thailand</strong> — hot season, get ready for Songkran.</li>
<li><strong>Georgia</strong> — early spring, mountains.</li>
<li><strong>Vietnam</strong> — southern beaches.</li>
</ul>
""",
    },
    "april": {
        "hero_image": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=1600&q=80",
        "destinations": [
            {"slug": "turkey", "temp": "+18-25°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Тюльпаны", "Погода"], "highlights_en": ["Tulips", "Weather"],
             "description_ru": "Лучшее время для Стамбула. Цветение тюльпанов, комфортная температура.",
             "description_en": "Best time for Istanbul. Tulip bloom, comfortable temperature."},
            {"slug": "thailand", "temp": "+30-38°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Сонгкран", "Скидки"], "highlights_en": ["Songkran", "Discounts"],
             "description_ru": "Сонгкран — тайский Новый год. Водные фестивали, скидки.",
             "description_en": "Songkran — Thai New Year. Water festivals, discounts."},
            {"slug": "egypt", "temp": "+25-30°C", "budget_ru": "₽60 000", "budget_en": "$600", "highlights_ru": ["Пляжи", "Экскурсии"], "highlights_en": ["Beaches", "Excursions"],
             "description_ru": "Комфортная погода перед летней жарой.",
             "description_en": "Comfortable weather before summer heat."},
            {"slug": "georgia", "temp": "+12-18°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Цветение", "Горы"], "highlights_en": ["Blooming", "Mountains"],
             "description_ru": "Весна в горах. Цветение, свежий воздух.",
             "description_en": "Spring in the mountains. Blooming, fresh air."},
        ],
        "tips_ru": "<h2>Куда поехать в апреле</h2><p>Апрель — идеальный месяц для путешествий. Не жарко, цены умеренные.</p>",
        "tips_en": "<h2>Where to Go in April</h2><p>April is ideal for travel. Not hot, moderate prices.</p>",
    },
    "may": {
        "hero_image": "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=1600&q=80",
        "destinations": [
            {"slug": "greece", "temp": "+22-28°C", "budget_ru": "₽80 000", "budget_en": "$800", "highlights_ru": ["Острова", "Кухня"], "highlights_en": ["Islands", "Food"],
             "description_ru": "Начало сезона. Тёплое море, мало туристов.",
             "description_en": "Start of season. Warm sea, few tourists."},
            {"slug": "turkey", "temp": "+22-28°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Пляжи", "Экскурсии"], "highlights_en": ["Beaches", "Excursions"],
             "description_ru": "Начало пляжного сезона. Комфортная температура.",
             "description_en": "Start of beach season. Comfortable temperature."},
            {"slug": "vietnam", "temp": "+28-33°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Пляжи", "Еда"], "highlights_en": ["Beaches", "Food"],
             "description_ru": "Юг: сухой сезон. Центр: начало дождей.",
             "description_en": "South: dry season. Central: start of rains."},
        ],
        "tips_ru": "<h2>Куда поехать в мае</h2><p>Май — межсезонье. Отличные цены, комфортная погода.</p>",
        "tips_en": "<h2>Where to Go in May</h2><p>May is off-season. Great prices, comfortable weather.</p>",
    },
    "june": {
        "hero_image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80",
        "destinations": [
            {"slug": "turkey", "temp": "+28-35°C", "budget_ru": "₽90 000", "budget_en": "$900", "highlights_ru": ["Пляжи", "All Inclusive"], "highlights_en": ["Beaches", "All Inclusive"],
             "description_ru": "Начало пляжного сезона. Море тёплое, цены растут.",
             "description_en": "Start of beach season. Warm sea, prices rising."},
            {"slug": "egypt", "temp": "+30-35°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Дайвинг", "Пляжи"], "highlights_en": ["Diving", "Beaches"],
             "description_ru": "Жарко, но море тёплое. Дайвинг в Красном море.",
             "description_en": "Hot, but warm sea. Red Sea diving."},
            {"slug": "montenegro", "temp": "+25-30°C", "budget_ru": "₽60 000", "budget_en": "$600", "highlights_ru": ["Адриатика", "Горы"], "highlights_en": ["Adriatic", "Mountains"],
             "description_ru": "Начало сезона. Кристальное море, горы.",
             "description_en": "Start of season. Crystal sea, mountains."},
        ],
        "tips_ru": "<h2>Куда поехать в июне</h2><p>Июнь — начало лета. Отличное время для пляжного отдыха.</p>",
        "tips_en": "<h2>Where to Go in June</h2><p>June is start of summer. Great time for beach vacation.</p>",
    },
    "july": {
        "hero_image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80",
        "destinations": [
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽200 000", "budget_en": "$2 000", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Влажный сезон, но дожди кратковременные. Цены ниже на 30-50%.",
             "description_en": "Wet season, but short showers. Prices 30-50% lower."},
            {"slug": "georgia", "temp": "+25-35°C", "budget_ru": "₽50 000", "budget_en": "$500", "highlights_ru": ["Горы", "Вино"], "highlights_en": ["Mountains", "Wine"],
             "description_ru": "Идеально для гор. Треккинг, фестивали, вино.",
             "description_en": "Perfect for mountains. Trekking, festivals, wine."},
            {"slug": "montenegro", "temp": "+28-35°C", "budget_ru": "₽80 000", "budget_en": "$800", "highlights_ru": ["Пляжи", "Яхтинг"], "highlights_en": ["Beaches", "Yachting"],
             "description_ru": "Пик сезона. Адриатическое море, яхтинг.",
             "description_en": "Peak season. Adriatic Sea, yachting."},
        ],
        "tips_ru": "<h2>Куда поехать в июле</h2><p>Июль — разгар лета. Много направлений в высоком сезоне.</p>",
        "tips_en": "<h2>Where to Go in July</h2><p>July is peak summer. Many destinations in high season.</p>",
    },
    "august": {
        "hero_image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80",
        "destinations": [
            {"slug": "georgia", "temp": "+25-35°C", "budget_ru": "₽50 000", "budget_en": "$500", "highlights_ru": ["Горы", "Вино"], "highlights_en": ["Mountains", "Wine"],
             "description_ru": "Сбор винограда. Свежее вино, горные фестивали.",
             "description_en": "Grape harvest. Fresh wine, mountain festivals."},
            {"slug": "montenegro", "temp": "+28-35°C", "budget_ru": "₽80 000", "budget_en": "$800", "highlights_ru": ["Пляжи", "Ночная жизнь"], "highlights_en": ["Beaches", "Nightlife"],
             "description_ru": "Пик сезона. Самое тёплое море.",
             "description_en": "Peak season. Warmest sea."},
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽200 000", "budget_en": "$2 000", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Влажный сезон. Дешевле, чем зимой.",
             "description_en": "Wet season. Cheaper than winter."},
        ],
        "tips_ru": "<h2>Куда поехать в августе</h2><p>Август — последний месяц лета. Ещё можно успеть на пляж.</p>",
        "tips_en": "<h2>Where to Go in August</h2><p>August is the last month of summer. Still time for the beach.</p>",
    },
    "september": {
        "hero_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1600&q=80",
        "destinations": [
            {"slug": "turkey", "temp": "+25-30°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Бархатный сезон", "Тёплое море"], "highlights_en": ["Velvet season", "Warm sea"],
             "description_ru": "Бархатный сезон. Тёплое море, меньше туристов, снижение цен.",
             "description_en": "Velvet season. Warm sea, fewer tourists, price drops."},
            {"slug": "egypt", "temp": "+28-33°C", "budget_ru": "₽50 000", "budget_en": "$500", "highlights_ru": ["Дайвинг", "Бюджетно"], "highlights_en": ["Diving", "Budget"],
             "description_ru": "Цены падают. Море тёплое, дайвинг отличный.",
             "description_en": "Prices drop. Warm sea, great diving."},
            {"slug": "georgia", "temp": "+18-25°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Вино", "Золотые горы"], "highlights_en": ["Wine", "Golden mountains"],
             "description_ru": "Сбор винограда. Свежее вино, золотые краски.",
             "description_en": "Grape harvest. Fresh wine, golden colors."},
        ],
        "tips_ru": "<h2>Куда поехать в сентябре</h2><p>Сентябрь — бархатный сезон. Идеальное время для бюджетного отдыха.</p>",
        "tips_en": "<h2>Where to Go in September</h2><p>September is velvet season. Ideal for budget travel.</p>",
    },
    "october": {
        "hero_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1600&q=80",
        "destinations": [
            {"slug": "turkey", "temp": "+20-28°C", "budget_ru": "₽60 000", "budget_en": "$600", "highlights_ru": ["Экскурсии", "Бюджетно"], "highlights_en": ["Sightseeing", "Budget"],
             "description_ru": "Конец сезона. Мало туристов, низкие цены.",
             "description_en": "End of season. Few tourists, low prices."},
            {"slug": "egypt", "temp": "+25-30°C", "budget_ru": "₽50 000", "budget_en": "$500", "highlights_ru": ["Дайвинг", "Экскурсии"], "highlights_en": ["Diving", "Excursions"],
             "description_ru": "Начало высокого сезона. Комфортная погода.",
             "description_en": "Start of high season. Comfortable weather."},
            {"slug": "vietnam", "temp": "+25-30°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Пляжи", "Еда"], "highlights_en": ["Beaches", "Food"],
             "description_ru": "Сухой сезон на юге. Идеально для Фукуока.",
             "description_en": "Dry season in the south. Perfect for Phu Quoc."},
        ],
        "tips_ru": "<h2>Куда поехать в октябре</h2><p>Октябрь — переходный месяц. Отличные цены на многие направления.</p>",
        "tips_en": "<h2>Where to Go in October</h2><p>October is a transition month. Great prices for many destinations.</p>",
    },
    "november": {
        "hero_image": "https://images.unsplash.com/photo-1548263594-a71f2df4da24?w=1600&q=80",
        "destinations": [
            {"slug": "thailand", "temp": "+28-32°C", "budget_ru": "₽90 000", "budget_en": "$900", "highlights_ru": ["Пляжи", "Начало сезона"], "highlights_en": ["Beaches", "Start of season"],
             "description_ru": "Начало высокого сезона. Идеальная погода.",
             "description_en": "Start of high season. Perfect weather."},
            {"slug": "egypt", "temp": "+22-28°C", "budget_ru": "₽70 000", "budget_en": "$700", "highlights_ru": ["Пляжи", "Экскурсии"], "highlights_en": ["Beaches", "Excursions"],
             "description_ru": "Высокий сезон. Комфортная погода.",
             "description_en": "High season. Comfortable weather."},
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽250 000", "budget_en": "$2 500", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Начало сухого сезона. Идеально для дайвинга.",
             "description_en": "Start of dry season. Perfect for diving."},
        ],
        "tips_ru": "<h2>Куда поехать в ноябре</h2><p>Ноябрь — начало сезона в Азии и на Ближнем Востоке.</p>",
        "tips_en": "<h2>Where to Go in November</h2><p>November is start of season in Asia and Middle East.</p>",
    },
    "december": {
        "hero_image": "https://images.unsplash.com/photo-1548263594-a71f2df4da24?w=1600&q=80",
        "destinations": [
            {"slug": "thailand", "temp": "+28-32°C", "budget_ru": "₽100 000", "budget_en": "$1 000", "highlights_ru": ["Пляжи", "Новый год"], "highlights_en": ["Beaches", "New Year"],
             "description_ru": "Высокий сезон. Новогодние каникулы — популярное время.",
             "description_en": "Peak season. New Year holidays — popular time."},
            {"slug": "maldives", "temp": "+27-30°C", "budget_ru": "₽300 000", "budget_en": "$3 000", "highlights_ru": ["Дайвинг", "Романтика"], "highlights_en": ["Diving", "Romance"],
             "description_ru": "Сухой сезон. Идеально для Нового года.",
             "description_en": "Dry season. Perfect for New Year."},
            {"slug": "uae", "temp": "+22-25°C", "budget_ru": "₽100 000", "budget_en": "$1 000", "highlights_ru": ["Шопинг", "Новый год"], "highlights_en": ["Shopping", "New Year"],
             "description_ru": "Новогодние распродажи. Фейерверки в Дубае.",
             "description_en": "New Year sales. Fireworks in Dubai."},
            {"slug": "georgia", "temp": "+2-8°C", "budget_ru": "₽40 000", "budget_en": "$400", "highlights_ru": ["Горные лыжи", "Новый год"], "highlights_en": ["Skiing", "New Year"],
             "description_ru": "Зимний отдых. Горные лыжи, новогодняя Тбилиси.",
             "description_en": "Winter vacation. Skiing, New Year in Tbilisi."},
        ],
        "tips_ru": "<h2>Куда поехать в декабре</h2><p>Декабрь — Новогодние каникулы. Самое популярное время для путешествий.</p>",
        "tips_en": "<h2>Where to Go in December</h2><p>December is New Year holidays. Most popular travel time.</p>",
    },
}


def build_seasonal_page(month_slug, lang):
    """Build a seasonal page for a specific month."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    SITE_DIR = Path(__file__).parent / "site"
    TEMPLATES_DIR = SITE_DIR / "templates"

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    env.globals["site_url"] = os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")
    from urllib.parse import urlparse as _urlparse
    _env_root = _urlparse(os.getenv("SITE_URL", "https://antondrakon.github.io/travel-content-site")).path.rstrip("/")
    env.globals["root"] = _env_root
    env.globals["formspree_id"] = "xnjyjnnd"
    env.globals["enumerate"] = enumerate

    # Analytics
    env.globals["analytics_enabled"] = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"
    env.globals["yandex_metrika_id"] = os.getenv("YANDEX_METRIKA_ID", None)
    env.globals["google_analytics_id"] = os.getenv("GOOGLE_ANALYTICS_ID", None)
    env.globals["recaptcha_site_key"] = os.getenv("RECAPTCHA_SITE_KEY", None)

    from datetime import date
    env.globals["current_year"] = str(date.today().year)

    # Destinations list
    from publisher import DESTINATIONS_LIST
    env.globals["destinations_list"] = DESTINATIONS_LIST
    env.globals["russia_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "russia"]
    env.globals["international_destinations"] = [d for d in DESTINATIONS_LIST if d["group"] == "international"]

    month_data = MONTHS[month_slug]
    seasonal = SEASONAL_DATA[month_slug]

    month_name_ru = month_data["ru"]
    month_name_en = month_data["en"]

    if lang == "ru":
        title = f"Куда поехать в {month_name_ru} 2026 — Лучшие направления"
        meta_description = f"Лучшие направления для отдыха в {month_name_ru} 2026. Погода, цены, советы."
        subtitle = f"Найдите идеальное направление для {month_name_ru.lower()}"
    else:
        title = f"Best Places to Visit in {month_name_en} 2026"
        meta_description = f"Best travel destinations for {month_name_en} 2026. Weather, prices, tips."
        subtitle = f"Find the perfect destination for {month_name_en}"

    # Build destination cards with images
    from publisher import get_country_image
    destinations = []
    for dest in seasonal["destinations"]:
        from config.destinations import DESTINATIONS
        country = DESTINATIONS.get(dest["slug"], {})
        destinations.append({
            "slug": dest["slug"],
            "name_ru": country.get("name_ru", dest["slug"]),
            "name_en": country.get("name_en", dest["slug"].title()),
            "temp": dest["temp"],
            "budget_ru": dest["budget_ru"],
            "budget_en": dest["budget_en"],
            "highlights_ru": dest.get("highlights_ru", []),
            "highlights_en": dest.get("highlights_en", []),
            "description_ru": dest["description_ru"],
            "description_en": dest["description_en"],
            "image": get_country_image(dest["slug"]),
            "emoji": get_country_emoji(dest["slug"]),
        })

    # Month navigation
    months_nav = []
    for m_slug, m_data in MONTHS.items():
        months_nav.append({
            "slug": m_slug,
            "name_ru": m_data["ru"],
            "name_en": m_data["en"],
            "emoji": m_data["emoji"],
        })

    tips = seasonal.get("tips_ru", "") if lang == "ru" else seasonal.get("tips_en", "")

    template = env.get_template("seasonal.html")
    html = template.render(
        lang=lang,
        title=title,
        meta_description=meta_description,
        subtitle=subtitle,
        hero_image=seasonal["hero_image"],
        month_slug=month_slug,
        month_name_ru=month_name_ru,
        month_name_en=month_name_en,
        destinations=destinations,
        tips=tips,
        months_nav=months_nav,
        alternate_url=f"seasonal/{month_slug}.html",
    )

    out = OUTPUT_DIR / lang / "seasonal" / f"{month_slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  Built: {out}")


def get_country_emoji(slug):
    emojis = {
        "russia": "🇷🇺", "baikal": "💎", "altai": "🏔", "karelia": "🌲",
        "dagestan": "⛰️", "kamchatka": "🌋", "mineral-vody": "♨️", "vladivostok": "⚓",
        "turkey": "🇹🇷", "thailand": "🇹🇭", "egypt": "🇪🇬",
        "uae": "🇦🇪", "indonesia": "🇮🇩", "china": "🇨🇳", "maldives": "🇲🇻",
        "sri-lanka": "🇱🇰", "montenegro": "🇲🇪", "vietnam": "🇻🇳",
        "georgia": "🇬🇪", "cyprus": "🇨🇾", "oman": "🇴🇲",
    }
    return emojis.get(slug, "🌍")


def build_all_seasonal():
    """Build all seasonal pages for all languages."""
    print("\n=== Building seasonal pages ===\n")

    for month_slug in MONTHS:
        for lang in ["ru", "en"]:
            build_seasonal_page(month_slug, lang)

    print("\n=== Seasonal pages done ===\n")


if __name__ == "__main__":
    build_all_seasonal()
