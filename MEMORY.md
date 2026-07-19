# MEMORY.md — Журнал проекта Travel Content Factory 2.0

## Версия: 2.0 (12-агентная система)

### Архитектура

Проект — автоматизированная редакция туристического портала с 12 AI-агентами.

**Стек**: Python 3.12, DeepSeek API (OpenAI-compatible), Jinja2, Tailwind CSS 4.x, Travelpayouts

**Масштаб**: 21 страна/регион, ~80 городов, 5 типов контента × 2 языка = ~800 потенциальных статей

---

## Реализовано (2026-07-19)

### Phase 1: Расширение партнёрской конфигурации

**Файл**: `config/affiliates.py`

| Параметр | Было | Стало |
|----------|------|-------|
| Сервисов | 17 | 54 |
| Категорий | 4 | 20 |
| Генераторов ссылок | 5 | 15+ |

**Новые категории**:
- Экскурсии (WeGoTrip, Tripster, GetYourGuide, Viator, Klook)
- Трансферы (Kiwitaxi, GetTransfer, Intui)
- eSIM (Airalo, YesIM, DrimSIM)
- Аренда авто (DiscoverCars, Localrent, GetRentACar, EconomyBookings, QEEQ, AutoEurope)
- Мото/велосипеды (BikesBooking)
- Билеты (Tiqets, Sputnik8, TicketNetwork)
- ЖД (Туту.ру, ВИП-зал)
- Автобусы (Юникей, 12Go)
- Круизы (Круиз Онлайн)
- Санатории (Санаторий, Sanatoriums.com)
- Кемпинги (МирТурбаз)
- Хранение багажа (Radical Storage)
- Яхты (Searadar)
- Компенсации (AirHelp, Compensair)
- Портал (Яндекс Путешествия)
- Маркетплейс (Авито)

**Обновлённые файлы**:
- `publisher.py` — импорт из `config/affiliates.py`, `linkify_services()` использует aliases из реестра
- `main.py` — `build_prompt()` передаёт новые плейсхолдеры
- `agents/affiliate_matcher.py` — обработка 10+ плейсхолдеров (hotels, flights, tours, excursions, transfers, esim, car_rental, insurance, tickets)
- `config/prompts.py` — промпты расширены секциями: экскурсии, трансфер, eSIM, страховка

---

### Phase 2: Новые агенты (5 шт.)

#### AGENT 1 — Project Analyzer
**Файл**: `agents/project_analyzer.py`

| Функция | Описание |
|---------|----------|
| `analyze_coverage()` | Сравнение DESTINATIONS с существующими JSON |
| `analyze_staleness()` | Проверка дат модификации (>30 дней) |
| `analyze_affiliate_coverage()` | Подсчёт категорий партнёрок в статьях |
| `analyze_internal_links()` | Граф ссылок между статьями |
| `generate_report()` | Полный отчёт с приоритетами |

#### AGENT 2 — Content Architect
**Файл**: `agents/content_architect.py`

| Функция | Описание |
|---------|----------|
| `plan_content_hierarchy()` | Планирование иерархии контента |
| `validate_hierarchy()` | Проверка структуры страны→город→тип |
| `suggest_content_gaps()` | Анализ пропущенного контента |
| `generate_content_calendar()` | Приоритизированный список генерации |

#### AGENT 3 — Fact Checker (улучшенный)
**Файл**: `agents/fact_checker.py`

| Параметр | Было | Стало |
|----------|------|-------|
| Стран с фактами | 7 | 21 |
| Типы проверок | regex | visa, currency, airports, timezone, prices, names |

**KNOWN_FACTS для всех 21 стран**: visa, currency (code/name/symbol), timezone, airports, driving_side, plug_type, emergency, alcohol, language

**Порог цен**: $0.10 (был $1.00 — слишком строго)

#### AGENT 7 — Internal Link Builder
**Файл**: `agents/internal_link_builder.py`

| Функция | Описание |
|---------|----------|
| `build_link_graph()` | Граф всех статей с их связями |
| `suggest_related()` | Предложение связанных статей (score-based) |
| `inject_related_section()` | Вставка секции "Похожие статьи" |
| `inject_contextual_links()` | Контекстные ссылки в теле статьи |

**Алгоритм scoring**: same_city_different_type (+50), same_country (+30), heading_overlap (+3-20), same_content_type (+15)

#### AGENT 8 — UX Copywriter
**Файл**: `agents/ux_copywriter.py`

| Функция | Описание |
|---------|----------|
| `remove_ai_fingerprints()` | Удаление AI-штампов (RU + EN) |
| `validate_structure()` | Проверка H2/H3 иерархии, длины абзацев |
| `check_cta_presence()` | Проверка наличия CTA и партнёрок |
| `enhance_readability()` | Анализ читаемости |
| `break_long_paragraphs()` | Автоматическое разбиение длинных абзацев |

**AI-штампы для удаления** (20+ паттернов RU, 18+ EN): "В заключение", "Подводя итог", "In conclusion", "Furthermore" и т.д.

---

### Phase 4: Pipeline Orchestrator

**Файл**: `agents/pipeline.py`

7-шаговый pipeline с retry logic (MAX_RETRIES=2):

```
1. Travel Writer → генерация черновика
2. Fact Checker → проверка фактов (retry при критических)
3. SEO Optimizer → оптимизация структуры
4. Affiliate Engine → внедрение партнёрских блоков
5. Internal Link Builder → добавление кросс-ссылок
6. UX Copywriter → полировка (AI fingerprints + paragraph breaking)
7. Save → сохранение JSON
```

**CLI команды**:
```bash
python main.py pipeline --country turkey --city istanbul --type guide --lang ru
python main.py pipeline --country turkey --lang both --force
python main.py analyze
python main.py plan --country turkey
python main.py qa --agent fact|seo|ux|links|images|all
```

---

### Исправления багов

| Баг | Причина | Исправление |
|-----|---------|-------------|
| `unhashable type: 'dict'` | Итерация `.items()` без распаковки | `for city_slug, city_data in ...` |
| `NameError: re` | Отсутствовал import в project_analyzer | Добавлен `import re` |
| Slug mismatch | content_architect генерировал `istanbul-flights` вместо `istanbul-cheap-flights` | Использование `seo_optimizer.get_url_slug()` |
| Price threshold | $0.2-0.5 — валидные цены для чая/снеков | Порог понижен до $0.10 |
| Long paragraphs | AI генерирует абзацы >500 символов | Добавлен `break_long_paragraphs()` |
| Missing currency/timezone | Промпты не содержали этих данных | Добавлены секции "Валюта" и "Часовой пояс" |
| Orphan heading false positives | H2→H3 считался orphan | Теперь orphan = same-level (H2→H2, H3→H3) |
| validate_structure regex | `re.split(r'</p>')` считал неправильно | Заменено на `re.findall(r'<p>(.*?)</p>')` |
| --force не сохранял | `if not out_path.exists()` guard | Удалён guard — всегда сохранять |
| Fact checker too strict | visa/airports/timezone для всех типов | Context-aware: только для guide |

---

## Статус покрытия Турции

| Город | RU | EN | Всего |
|-------|----|----|-------|
| Istanbul | 5/5 | 5/5 | 10/10 ✓ |
| Antalya | 5/5 | 5/5 | 10/10 ✓ |
| Bodrum | 5/5 | 5/5 | 10/10 ✓ |
| Cappadocia | 5/5 | 5/5 | 10/10 ✓ |
| **Итого** | **20/20** | **20/20** | **40/40 ✓** |

---

## Оставшиеся проблемы

| Проблема | Приоритет | Решение |
|----------|-----------|---------|
| break_long_paragraphs работает в изоляции, но pipeline-файлы всё ещё длинные | Высокий | Debug output добавлен — нужно запустить pipeline и проверить логи |
| Fact checker: currency TRY не упомянута в не-guide статьях | Средний | AI не всегда включает currency в промпт — возможно усилить промпт |
| 360 статей старше 30 дней | Средний | Запуск `pipeline --force` для обновления |

---

## Следующие шаги

1. Разобраться с багом break_long_paragraphs в pipeline (debug output уже добавлен)
2. Добавить автоматическое переписывание длинных абзацев через AI
3. Реализовать gate-check: статья не публикуется пока все агенты не PASS
4. Добавить CI/CD pipeline для автоматической генерации
5. Расширить покрытие на остальные 17 стран

---

## Структура файлов

```
travel-content-factory/
├── agents/
│   ├── pipeline.py              # Мастер-оркестратор (новый)
│   ├── project_analyzer.py      # AGENT 1 (новый)
│   ├── content_architect.py     # AGENT 2 (новый)
│   ├── fact_checker.py          # AGENT 3 (улучшенный)
│   ├── internal_link_builder.py # AGENT 7 (новый)
│   ├── ux_copywriter.py         # AGENT 8 (новый)
│   ├── content_writer.py        # AGENT 5 (Travel Writer)
│   ├── seo_optimizer.py         # AGENT 4 (SEO Strategist)
│   ├── affiliate_matcher.py     # AGENT 6 (обновлён)
│   ├── link_agent.py            # Валидация ссылок
│   ├── image_agent.py           # Аудит изображений
│   ├── copy_seo_agent.py        # SEO аудит
│   ├── ux_performance_agent.py  # UX/Performance аудит
│   ├── qa_manager.py            # QA оркестратор
│   ├── image_injector.py        # Инъекция каруселей
│   ├── hotel_photo_fetcher.py   # Загрузка фото отелей
│   └── hotel_image_agent.py     # Агент фото отелей
├── config/
│   ├── affiliates.py            # Реестр 54 сервисов (обновлён)
│   ├── destinations.py          # 21 страна, ~80 городов
│   ├── prompts.py               # Промпты с плейсхолдерами (обновлён)
│   └── country_data.py          # Данные по странам
├── photo_pipeline/              # Модульный пайплайн фото
├── main.py                      # CLI точка входа (обновлён)
├── publisher.py                 # Генератор HTML (обновлён)
└── content/                     # Сгенерированный контент
    ├── ru/                      # Русские статьи
    └── en/                      # Английские статьи
```

---

## Структура главной страницы (home.html)

| # | Секция | Описание |
|---|--------|----------|
| 1 | HERO | 75vh, фото пляжа, заголовок, поиск, 10 быстрых ссылок |
| 2 | СТРАНЫ | 3-col grid, 21 карточка страны |
| 3 | РОССИЯ | 4-col grid, 8 карточек российских направлений |
| 4 | ЗАРУБЕЖЬЕ | 4-col grid, 8 популярных международных направлений |
| 5 | ОТЕЛИ | 4-col grid, 8 популярных отелей с ценами и рейтингами |
| 6 | СЕЗОННЫЕ | 3-col grid, "Куда поехать летом" |
| 7 | ПОДБОРКИ | Горизонтальный скролл, 6 категорий |
| 8 | СТАТЬИ | 3-col grid, 3 карточки путеводителей |
| 9 | ФОРМА | Agent form с benefits |
| 10 | FAQ | 8 вопросов (RU/EN) |
| 11 | NEWSLETTER + RSS | Форма подписки + RSS-ссылка |

---

## Дата последнего обновления: 2026-07-19
