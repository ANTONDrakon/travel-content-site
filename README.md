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
│   ├── destinations.py  # 5 стран, 25 городов
│   ├── prompts.py       # Промпты (RU + EN)
│   └── affiliates.py    # Партнёрские ссылки Travelpayouts
├── agents/
│   ├── content_writer.py    # DeepSeek API
│   ├── seo_optimizer.py     # SEO-метаданные
│   └── affiliate_matcher.py # Вставка партнёрок
├── site/templates/      # Jinja2-шаблоны
├── content/             # Сгенерированные статьи (JSON)
└── docs/                # Готовый сайт для GitHub Pages
```

## Быстрый старт

### 1. Установка

```bash
pip install -r requirements.txt
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

# Сгенерировать ВСЁ (5 стран × 5 городов × 5 типов × 2 языка = 250 статей)
python main.py generate --lang both
```

### 4. Сборка сайта

```bash
python main.py build
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
| `python main.py build` | Собрать сайт |
| `python main.py all` | Сгенерировать ВСЁ + собрать сайт |

## Монетизация

Проект использует **Travelpayouts** для партнёрских ссылок:
- Отели — Hotellook (комиссия 4-8%)
- Авиабилеты — Aviasales (комиссия 2-4%)
- Туры — Level.Travel (комиссия 3-5%)
- Страховки — Cherehapa (комиссия 10-15%)

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
