# 🌍 AI Travel Content Factory

Автоматическая система генерации туристического контента с SEO-оптимизацией и партнёрскими ссылками.

## Что делает

- **Генерирует статьи** через DeepSeek AI на русском и английском
- Внедряет **партнёрские ссылки** Travelpayouts (отели, билеты, туры, страховки)
- Оптимизирует **SEO**: meta, schema.org, hreflang, sitemap
- Собирает **статический сайт** на Tailwind CSS
- Публикует на **GitHub Pages** (бесплатно)

## Структура

```
travel-content-factory/
├── main.py              # CLI: python main.py generate|build|all
├── publisher.py         # Сборка HTML-сайта (Jinja2)
├── sitemap_generator.py # Генерация sitemap.xml
├── config/
│   ├── destinations.py  # 21 страна/регион, ~80 городов
│   ├── prompts.py       # Промпты (RU + EN)
│   ├── affiliates.py    # Партнёрские ссылки Travelpayouts
│   └── country_data.py  # Подробные данные по странам
├── agents/
│   ├── content_writer.py    # DeepSeek API
│   ├── seo_optimizer.py     # SEO-метаданные
│   ├── affiliate_matcher.py # Вставка партнёрок
│   └── image_injector.py    # Инъекция фото отелей
├── site/templates/      # Jinja2-шаблоны
├── content/             # Сгенерированные статьи (JSON)
└── docs/                # Готовый сайт для GitHub Pages
```

## Направления

### Россия (приоритет)
- **Москва**, **Санкт-Петербург**, **Сочи**, **Калининград**, **Казань**
- **Байкал** (Иркутск, Листвянка, Ольхон)
- **Алтай** (Горно-Алтайск, Чемал, Аккем)
- **Карелия** (Петрозаводск, Сортавала, Кижи)
- **Дагестан** (Махачкала, Дербент, Кизляр)
- **Камчатка** (Петропавловск-Камчатский, Паратунка)
- **Кавказские Минеральные Воды** (Пятигорск, Кисловодск, Ессентуки)
- **Владивосток** (Владивосток, Русский остров)

### Зарубежные
- **Турция** (Стамбул, Анталья, Бодрум, Каппадокия)
- **Таиланд** (Бангкок, Пхукет, Паттайя, Самуи, Краби)
- **Египет** (Шарм-эль-Шейх, Хургада, Каир, Луксор, Марса-Алам)
- **ОАЭ** (Дубай, Абу-Даби, Шарджа, Рас-эль-Хайма, Фуджейра)
- **Индонезия** (Убуд, Кута, Семиньяк, Чангу, Нуса-Дуа)
- **Китай** (Санья, Хайкоу, Пекин, Шанхай, Сиань)
- **Мальдивы** (Мале, Маафуши, Хулхумале и др.)
- **Шри-Ланка**, **Черногория**, **Вьетнам**, **Грузия**, **Кипр**, **Оман**

## Быстрый старт

### 1. Установка

```bash
# Python зависимости
pip install -r requirements.txt

# Node.js зависимости (для Tailwind CSS)
npm install
```

### 2. Настройка

Создай `.env` файл:

```
DEEPSEEK_API_KEY=sk-ваш_ключ
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
TRAVELPAYOUTS_MARKER=736226
SITE_URL=https://ТВОЙ_ЮЗЕР.github.io/travel-content-site
```

### 3. Генерация контента

```bash
# Сгенерировать одну статью (гид по Стамбулу, русский)
python main.py generate --country turkey --city istanbul --type guide --lang ru

# Сгенерировать все 5 типов статей для Стамбула (RU + EN)
python main.py generate --country turkey --city istanbul --lang both

# Сгенерировать все статьи для Турции (5 городов × 5 типов × 2 языка = 50 статей)
python main.py generate --country turkey --lang both

# Сгенерировать ВСЁ (21 регион × ~80 городов × 5 типов × 2 языка)
python main.py generate --lang both
```

### 4. Сборка сайта

```bash
# Полная сборка (Tailwind CSS + HTML страницы)
python main.py build

# Или отдельно:
npm run tailwind:build   # Собрать Tailwind CSS
python publisher.py      # Собрать HTML страницы
```

Сайт будет собран в папку `docs/`.

### 5. Публикация на GitHub Pages

1. Залей код на GitHub
2. Settings → Pages → Source: `main` branch, `/docs` folder
3. Сайт будет доступен по адресу `https://ТВОЙ_ЮЗЕР.github.io/репозиторий`

## Команды

| Команда | Описание |
|---------|----------|
| `python main.py list` | Показать все направления |
| `python main.py generate --country turkey --lang both` | Сгенерировать контент для страны |
| `python main.py generate --country turkey --city istanbul --type guide --lang ru` | Одна статья |
| `python main.py build` | Собрать сайт (включая Tailwind CSS) |
| `python main.py all` | Сгенерировать ВСЁ + собрать сайт |
| `npm run tailwind:build` | Собрать Tailwind CSS (production) |
| `npm run tailwind:watch` | Watch-режим для разработки |

## Структура CSS

- `site/assets/input.css` — входной файл для Tailwind CSS
- `site/assets/styles.css` — кастомные стили (компоненты, анимации)
- `docs/assets/tailwind.css` — собранный Tailwind CSS (минифицированный, ~10KB)

## Монетизация

Проект использует **Travelpayouts** для партнёрских ссылок:
- Отели — Hotellook (комиссия 4-8%)
- Авиабилеты — Aviasales (комиссия 2-4%)
- Туры — Level.Travel (комиссия 3-5%)
- Страховки — Cherehapa (комиссия 10-15%)

## Аналитика

### Настройка

Добавь в `.env` файл:

```
ANALYTICS_ENABLED=true
YANDEX_METRIKA_ID=ваш_идентификатор
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

### Что отслеживается

- **Просмотры страниц** — автоматически
- **Клики по партнёрским ссылкам** — автоматически
- **Отправка форм** — автоматически
- **Прокрутка страницы** — 25%, 50%, 75%, 100%
- **Время на странице** — при уходе
- **Core Web Vitals** — FCP, LCP, CLS, TTFB, FID

### Инструменты

- **Яндекс.Метрика**: https://metrika.yandex.ru
- **Google Analytics**: https://analytics.google.com
- **Google Search Console**: https://search.google.com/search-console

## План развития

1. **Месяц 1**: 125 статей → 10-30 посетителей/день
2. **Месяц 2**: 300 статей → 50-100 посетителей/день
3. **Месяц 3**: 500 статей → 100-300 посетителей/день
4. **Месяц 6**: 1000+ статей → 500-1500 посетителей/день
5. **Месяц 12**: 2000+ статей → 1500-4000 посетителей/день

## Добавление новых стран

В `config/destinations.py` добавь новую страну по шаблону:

```python
"vietnam": {
    "name_ru": "Вьетнам",
    "name_en": "Vietnam",
    "slug": "vietnam",
    "currency": "VND",
    "visa_ru": "безвизовый въезд до 45 дней",
    "visa_en": "visa-free entry for up to 45 days",
    "airport_code": "SGN",
    "cities": {
        "hanoi": {
            "name_ru": "Ханой", "name_en": "Hanoi",
            "slug": "hanoi", "airport_codes": ["HAN"],
            "lat": 21.0278, "lon": 105.8342,
        },
        # ... ещё города
    },
},
```

Затем:
```bash
python main.py generate --country vietnam --lang both
python main.py build
```
