# PROJECT_MEMORY.md — AI Travel Content Factory

## Общая цель проекта

Автоматическая система генерации туристического контента с SEO-оптимизацией и партнёрскими ссылками Travelpayouts. Цель — коммерческий туристический сайт, приносящий доход через партнёрские программы и заявки на подбор туров.

**Стек:** Python 3.12, Jinja2, Tailwind CSS 4.x (production build), DeepSeek AI API, GitHub Pages / Netlify / Vercel
**Языки:** RU + EN + ES (трёхъязычный)
**Монетизация:** Travelpayouts (17 сервисов) + Formspree (заявки на туры)
**Направления:** 16 стран, ~80 городов, 5 типов контента на 3 языка = ~2400 статей потенциально
**Статус:** ✅ Редизайн v5.0 завершён. Все 945 страниц собраны. Деплой на Vercel + GitHub Pages.

---

## Структура проекта

```
travel-content-factory/
├── main.py                    # CLI: generate|build|all|list
├── publisher.py               # Сборка HTML-сайта (Jinja2, 800 строк)
├── sitemap_generator.py       # Генерация sitemap.xml
├── validate.py                # Валидация контента
├── verify_fixes.py            # Верификация исправлений
├── requirements.txt           # Зависимости
├── .env.example               # Шаблон переменных окружения
├── README.md                  # Документация
├── config/
│   ├── __init__.py
│   ├── destinations.py        # 21 страна/регион, ~80 городов
│   ├── prompts.py             # Промпты для AI (RU + EN)
│   ├── affiliates.py          # Генератор партнёрских ссылок
│   └── country_data.py        # Подробные данные по странам
├── agents/
│   ├── __init__.py
│   ├── content_writer.py      # DeepSeek API генерация
│   ├── seo_optimizer.py       # SEO-метаданные, Schema.org
│   ├── affiliate_matcher.py   # Вставка партнёрок в текст
│   ├── image_injector.py      # Инъекция фото отелей
│   ├── fact_agent.py          # Проверка фактов
│   ├── hotel_image_agent.py   # Агент фото отелей
│   ├── hotel_photo_fetcher.py # Загрузчик фото
│   ├── image_agent.py         # Агент изображений
│   ├── link_agent.py          # Агент ссылок
│   ├── copy_seo_agent.py      # SEO-копирайтинг
│   ├── ux_performance_agent.py# UX/производительность
│   └── qa_manager.py          # QA-менеджер
├── photo_pipeline/            # Пайплайн загрузки фото
│   ├── pipeline.py, cli.py, downloader.py, uploader.py
│   ├── providers/ (pixabay, pexels, booking, google_places, travelpayouts)
│   └── tests/
├── site/
│   ├── templates/ (base.html, home.html, article.html, destination-rich.html)
│   └── assets/robots.txt
├── content/                   # Сгенерированный контент (JSON)
│   ├── ru/{country}/{city}-{type}.json
│   └── en/{country}/{city}-{type}.json
├── docs/                      # Готовый сайт для GitHub Pages
│   ├── index.html (redirect)
│   ├── robots.txt
│   ├── sitemap.xml, sitemap-ru.xml, sitemap-en.xml
│   ├── ru/{country}/*.html
│   └── en/{country}/*.html
└── data/
    ├── hotels.json
    ├── hotel_photo_sources.json
    ├── cities.json
    └── countries.json
```

---

## Выполнено

* Полный анализ структуры проекта
* Анализ всех Python-файлов (main.py, publisher.py, sitemap_generator.py, agents/*, config/*)
* Анализ всех HTML-шаблонов (base.html, home.html, article.html, destination-rich.html)
* Анализ SEO-конфигурации (robots.txt, sitemap.xml, Schema.org, OpenGraph)
* Анализ партнёрских ссылок (Travelpayouts, структура URL)
* Анализ системы генерации контента (промпты, AI-пайплайн)

### Исправления (P0 — критические)
* **robots.txt**: Исправлен регистр URL `ANTONDrakon` → `antondrakon` в docs/robots.txt, docs/sitemap.xml, docs/sitemap-ru.xml, docs/sitemap-en.xml
* **sitemap_generator.py**: Исправлен дефолтный URL с `YOUR_USERNAME` на `antondrakon`
* **Schema.org**: Заменены захардкоженные даты на динамические `date.today().isoformat()`
* **404 страница**: Созданы EN и RU версии с навигацией и ссылками на направления
* **site/assets/robots.txt**: Удалён Jinja2-шаблон `{{ site_url }}`, заменён на статичный URL

### Исправления (P1 — важные)
* **base.html**: Добавлен `<meta name="theme-color">`, favicon, исправлены CSS-переменные
* Удалён неиспользуемый Swiper.js, нестандартные AI-мета-теги, дублирующий canonical
* Исправлен hreflang x-default: RU → EN
* Добавлен `logo` в Organization Schema.org

### Новые направления (Россия — 8 регионов, 24 населённых пункта)
* russia, baikal, altai, karelia, dagestan, kamchatka, mineral-vody, vladivostok
* Обновлены все шаблоны, publisher.py, country_data.py

### Улучшения (21-110)
* **IMPROVEMENTS.md**: Создан список 105 улучшений с приоритетами
* **about.html**: Создана страница "О нас" (EN + RU)
* **contacts.html**: Создана страница "Контакты" с формой и контактами
* **sitemap_generator.py**: Добавлены about/contacts в sitemap
* **base.html**: Добавлены preconnect/dns-prefetch для критических ресурсов
* **base.html**: Добавлен `scroll-behavior: smooth`
* **base.html**: Добавлен skip-to-content link для accessibility
* **base.html**: Обёрнуто содержимое в `<main id="main-content">`
* **base.html**: Улучшены стили form validation (border-radius, transition, :invalid)
* **base.html footer**: Добавлены ссылки на About/Contacts
* **country_data.py**: Исправлены опечатки (китайцами→китами, ancient ruins→древние руины, 无限ными→бескрайними)
* **site/assets/styles.css**: Вынесен CSS из base.html в отдельный файл (кэшируется браузером)
* **tailwind.config.js**: Создан конфиг Tailwind CSS
* **site/assets/input.css**: Создан входной файл для Tailwind CSS
* **package.json**: Добавлены npm-скрипты для сборки Tailwind
* **docs/assets/tailwind.css**: Собран production-билд Tailwind CSS (~10KB минифицированный)
* **base.html**: Заменён CDN `cdn.tailwindcss.com` на production-билд
* **publisher.py**: Добавлена автоматическая сборка Tailwind при `python main.py build`
* **.gitignore**: Добавлены node_modules/, package-lock.json
* **README.md**: Обновлены инструкции по установке и сборке
* **optimize_images.py**: Создан скрипт оптимизации изображений (WebP, сжатие, responsive)
* **base.html**: Добавлен lazy loading с Intersection Observer (100px preload)
* **site/assets/styles.css**: Добавлены CSS-анимации для lazy loading (fade-in)
* **destination-rich.html**: Добавлен `loading="lazy"` к фото агента
* **docs/assets/optimized/**: Оптимизировано 95 изображений (~1.8MB)
* **docs/assets/optimized/manifest.json**: Манифест оптимизированных изображений
* **minify_html.py**: Создана утилита минификации HTML/CSS/JS
* **publisher.py**: Добавлена автоматическая минификация HTML при сборке
* **site/assets/analytics.js**: Создан модуль аналитики (Yandex.Metrika, Google Analytics)
* **site/assets/perf-monitor.js**: Создан мониторинг производительности (Core Web Vitals)
* **base.html**: Добавлены скрипты аналитики и мониторинга
* **publisher.py**: Добавлена конфигурация аналитики в Jinja2
* **.env.example**: Добавлены переменные для аналитики
* **README.md**: Добавлена секция "Аналитика"
* **site/assets/robots.txt**: Добавлены Disallow для служебных папок
* **base.html**: Добавлен preload для критических ресурсов (CSS, шрифты)
* **site/assets/styles.css**: Добавлены focus-visible стили для accessibility
* **site/assets/styles.css**: Добавлены print стили для печати страниц
* **site/assets/styles.css**: Добавлены reduced-motion стили
* **site/assets/styles.css**: Добавлены responsive image стили
* **docs/sw.js**: Создан Service Worker для офлайн-кэширования
* **base.html**: Добавлена регистрация Service Worker
* **docs/.htaccess**: Создана конфигурация кэширования для Apache
* **netlify.toml**: Создана конфигурация для Netlify
* **base.html**: Улучшены OG теги (og:site_name, og:image:alt, twitter:site, twitter:title, twitter:description, twitter:image)
* **base.html**: Добавлен WebSite Schema с SearchAction
* **base.html**: Улучшен Organization Schema (foundingDate, areaServed, knowsAbout)
* **base.html**: Добавлен robots meta `max-snippet:-1, max-video-preview:-1`
* **base.html**: Добавлен meta author
* **destination-rich.html**: Добавлены og_title, og_description, og_image_alt, twitter теги
* **destination-rich.html**: Добавлен BreadcrumbList Schema
* **article.html**: Добавлены og_title, og_description, og_image_alt, twitter теги
* **article.html**: Добавлены article:published_time, article:modified_time, article:section, article:author
* **article.html**: Добавлено время чтения в мета-информацию
* **base.html**: Добавлен hamburger menu для мобильных устройств
* **base.html**: Добавлен reading progress bar
* **base.html**: Добавлен mobile menu с навигацией
* **article.html**: Добавлен Table of Contents (оглавление)
* **site/assets/styles.css**: Добавлены стили для hamburger menu, reading progress, TOC, dark mode
* **base.html**: Добавлен form success message при успешной отправке
* **site/assets/styles.css**: Добавлена поддержка dark mode через prefers-color-scheme
* **docs/sw.js**: Создан Service Worker для офлайн-кэширования
* **base.html**: Добавлена регистрация Service Worker
* **docs/.htaccess**: Создана конфигурация кэширования для Apache
* **netlify.toml**: Создана конфигурация для Netlify
* **base.html**: Улучшены OG теги (og:site_name, og:image:alt, twitter:site, twitter:title, twitter:description, twitter:image)
* **base.html**: Добавлен WebSite Schema с SearchAction
* **base.html**: Улучшен Organization Schema (foundingDate, areaServed, knowsAbout)
* **base.html**: Добавлен robots meta `max-snippet:-1, max-video-preview:-1`
* **base.html**: Добавлен meta author
* **destination-rich.html**: Добавлены og_title, og_description, og_image_alt, twitter теги
* **destination-rich.html**: Добавлен BreadcrumbList Schema
* **article.html**: Добавлены og_title, og_description, og_image_alt, twitter теги
* **article.html**: Добавлены article:published_time, article:modified_time, article:section, article:author
* **article.html**: Добавлено время чтения в мета-информацию
* **docs/sw.js**: Создан Service Worker для офлайн-кэширования
* **base.html**: Добавлена регистрация Service Worker
* **docs/.htaccess**: Создана конфигурация кэширования для Apache
* **netlify.toml**: Создана конфигурация для Netlify

---

## Выполняется

* Добавление международных направлений (Шри-Ланка, Грузия, Вьетнам, Черногория, Кипр, Оман — уже в destinations.py)
* Оптимизация производительности
* Добавление CAPTCHA на формы
* Персонализация FAQ по городам

---

## Найденные проблемы

### КРИТИЧЕСКИЕ (P0)

1. ~~**robots.txt — case inconsistency**~~ — ИСПРАВЛЕНО ранее
2. ~~**Schema.org dates hardcoded**~~ — ИСПРАВЛЕНО ранее (date.today())
3. ~~**Нет 404 страницы**~~ — ИСПРАВЛЕНО ранее
4. ~~**Нет файла .env**~~ — Остаётся: нужен .env с ключами API
5. ~~**megatec_output.html**~~ — Посторонний файл, не относится к проекту. Можно удалить.

6. ~~**article:published_time захардкожен**~~ — ИСПРАВЛЕНО: теперь date.today()
7. ~~**_fetch_exchange_rates() при импорте**~~ — ИСПРАВЛЕНО: lazy loading

### ВАЖНЫЕ (P1)

6. ~~**CDN Tailwind CSS**~~ — ИСПРАВЛЕНО ранее (production build)
7. ~~**Нет lazy loading для hero-изображений**~~ — ИСПРАВЛЕНО ранее
8. ~~**Formspree без CAPTCHA**~~ — ИСПРАВЛЕНО: добавлена reCAPTCHA v2 (RECAPTCHA_SITE_KEY в .env)
9. ~~**Мета-теги AI-контента**~~ — ИСПРАВЛЕНО ранее (удалены)
10. ~~**Нет OpenGraph image для всех стран**~~ — ИСПРАВЛЕНО: добавлены все 21 страна
11. ~~**CITY_IMAGES не покрывают все города**~~ — ИСПРАВЛЕНО: добавлены все ~80 городов
12. ~~**Нет hreflang для country index pages**~~ — Проверено: hreflang корректен (ложная тревога)
13. **Форма в footer не привязана к #agent-form** — Sticky CTA ведёт на #agent-form, но на страницах статей этот ID может отсутствовать.
14. ~~**Нет Breadcrumb Schema для country pages**~~ — ИСПРАВЛЕНО: BreadcrumbList уже добавлен в destination-rich.html

### СРЕДНИЕ (P2)

15. ~~**Дублирование CSS**~~ — ИСПРАВЛЕНО ранее (styles.css вынесен)
16. ~~**Swiper.js подключается, но не используется**~~ — ИСПРАВЛЕНО ранее (удалён из base.html, используется в image_injector.py)
17. ~~**Нет аналитики**~~ — ИСПРАВЛЕНО ранее (analytics.js, perf-monitor.js)
18. ~~**Нет favicon**~~ — ИСПРАВЛЕНО ранее (favicon.svg)
19. ~~**Нет Service Worker / PWA**~~ — ИСПРАВЛЕНО ранее (sw.js)
20. ~~**Copyright 2026**~~ — ИСПРАВЛЕНО: теперь динамический (current_year)
21. ~~**Copy-paste в template**~~ — ИСПРАВЛЕНО: создан централизованный DESTINATIONS_LIST в publisher.py, footer и формы используют циклы
22. ~~**FAQ генерируется статично**~~ — ИСПРАВЛЕНО: generate_faq() теперь принимает country_slug и city_slug, загружает данные из COUNTRY_DATA, предоставляет персонализированные ответы для каждого типа контента
23. ~~**Нет canonical на redirect page**~~ — ИСПРАВЛЕНО: добавлены canonical и noindex

21. **Нет мета-тега `theme-color`**: Для мобильных браузеров.

22. **Copy-paste в template**: Направления (Turkey, Thailand и др.) дублируются в home.html, base.html footer, и forms — нет единого источника.

23. **FAQ генерируется статично**: `generate_faq()` в `seo_optimizer.py` возвращает одинаковые ответы для всех городов одного типа. Нет персонализации.

24. **Нет страницы "О нас"**: Только текст в footer и agent-block.

25. **Нет страницы "Контакты"**: Только форма Formspree.

26. **Нет robots meta на некоторых страницах**: Проверить все сгенерированные страницы.

27. **Нет canonical на странице redirect**: `docs/index.html` не имеет canonical.

28. **Unsplash изображения могут блокироваться**: Unsplash может ограничивать hotlinking.

29. **Нет CSP (Content Security Policy)**: Нет заголовков безопасности.

30. **Нет structured data для Organization**: Только базовый `@type: Organization` в base.html, нет logo, social links.

### НИЗКИЕ (P3)

31. **Нет email-подписки**: Нет лид-магнита. Требуется интеграция с email-сервисом.

32. ~~**Нет seasonal pages**~~ — ИСПРАВЛЕНО: создан seasonal_generator.py, 12 месяцев x 2 языка = 24 страницы с рекомендациями, погодой, ценами, советами. Добавлены в build процесс и sitemap.

33. **Нет сравнения направлений**: Нет страниц "Турция vs Египет". Требуется генерация сравнительных статей.

34. **Нет блога**: Только сгенерированные статьи. Требуется добавление блог-секции.

35. ~~**Нет RSS-фида**~~ — ИСПРАВЛЕНО: создан rss_generator.py, RSS 2.0 для RU и EN, автоматически в build процессе

36. **Нет страницы "Партнёрам"**: Нет информации для потенциальных партнёров.

37. ~~**Нет breadcrumbs в JSON-LD для country pages**~~ — ИСПРАВЛЕНО ранее (destination-rich.html)

38. **Нет i18n для статических элементов**: "TravelHub", "Expert guide" и т.д. захардкожены.

39. ~~**Нет error handling в publisher.py**~~ — ИСПРАВЛЕНО: load_json() теперь обрабатывает corrupted JSON

40. **Нет тестов**: Только `photo_pipeline/tests/test_verifier.py`.

41. **article.html:17** — article:published_time захардкожен на "2026-01-15T10:00:00+03:00" для всех статей.

42. **publisher.py:68** — `_fetch_exchange_rates()` вызывается при импорте модуля — сетевой вызов при каждом `import publisher`.

43. **contacts.html** — Telegram ссылка была пустой (https://t.me/), исправлена.

44. **base.html** — Footer не содержал 8 направлений (КМВ, Владивосток, Шри-Ланка, Черногория, Вьетнам, Грузия, Кипр, Оман) — исправлено.

---

## Предложения

### По SEO

1. Добавить динамические даты публикации/обновления на основе файла JSON
2. Добавить hreflang для всех страниц (включая country index)
3. Добавить BreadcrumbList Schema для country pages
4. Убрать нестандартные AI-мета-теги или добавить пояснение
5. Добавить OpenGraph для всех стран и городов
6. Создать 404 страницу с навигацией
7. Добавить canonical на redirect page
8. Добавить мета-тег theme-color

### По UX/UI

9. Вынести CSS в отдельный файл для кэширования
10. Убрать неиспользуемый Swiper.js
11. Добавить lazy loading для hero-изображений
12. Добавить favicon
13. Добавить плавные анимации появления секций
14. Улучшить мобильную навигацию (hamburger menu)
15. Добавить "Наверх" кнопку с плавной прокруткой (уже есть, но можно улучшить)

### По коммерциализации

16. Добавить лид-магнит (PDF-гайд, чек-лист)
17. Добавить email-подписку
18. Добавить seasonal pages для сезонного трафика
19. Добавить страницы сравнений направлений
20. Добавить RSS-фид

### По контенту

21. Добавить российские направления (Москва, СПб, Сочи, Калининград и др.)
22. Добавить международные направления (Шри-Ланка, Грузия и др.)
23. Персонализировать FAQ по городам
24. Добавить страницу "О нас" с историей и командой

### По безопасности

25. Добавить CAPTCHA на формы
26. Добавить CSP заголовки
27. Добавить .env в .gitignore (проверить)

---

## Следующие шаги

1. ~~Исправить критические проблемы (P0)~~ ✅
2. ~~Исправить важные проблемы (P1)~~ ✅
3. **Рефакторинг копипасты в шаблонах** (P2) — дедупликация списков направлений в base.html footer, agent form, home.html form, destination-rich.html form, contacts.html form
4. Персонализировать FAQ по городам (P2)
5. Добавить CSP заголовки (P3)
6. Добавить лид-магнит и email-подписку (P4)

---

## Исправленные ошибки

1. Регистр URL в robots.txt и sitemap.xml (ANTONDrakon → antondrakon)
2. Захардкоженные даты в Schema.org (2026-01-15 → date.today())
3. Отсутствие 404 страницы
4. Jinja2-шаблон в robots.txt без обработки
5. Несуществующая CSS-переменная `var(--vermillion)` → `var(--teal)`
6. Дублирующий canonical тег в base.html
7. Неправильный hreflang x-default (RU → EN)
8. Неиспользуемый Swiper.js подключался но не применялся
9. Нестандартные AI-мета-теги не reconocidos por buscadores
10. Отсутствие favicon и theme-color
11. Опечатки в country_data.py (китайцами, ancient ruins, 无限ными)
12. Отсутствие preconnect критических ресурсов
13. Отсутствие smooth scroll behavior
14. Отсутствие accessibility skip-to-content link
15. **publisher.py:185** — Опечатка "cănзуется" → "требуется" в инструкции по QR-коду для Китая
16. **publisher.py** — Bare `except:` (4 штуки) заменены на `except (ValueError, KeyError, TypeError):` для корректного error handling
17. **base.html footer** — Добавлены недостающие направления в footer: КМВ, Владивосток, Шри-Ланка, Черногория, Вьетнам, Грузия, Кипр, Оман (всего 22 направления вместо 13)
18. **contacts.html** — Добавлены WhatsApp как способ связи, исправлена ссылка Telegram
19. **article.html** — article:published_time и article:modified_time теперь динамические (date.today()), текст "Updated: July 2026" тоже динамический
20. **publisher.py** — `_fetch_exchange_rates()` переведён на lazy loading (не вызывается при импорте модуля)
21. **publisher.py CITY_IMAGES** — Добавлены 55 недостающих городов (Россия, Байкал, Алтай, Карелия, Дагестан, Камчатка, КМВ, Владивосток, Шри-Ланка, Черногория, Вьетнам, Грузия, Кипр, Оман)
22. **publisher.py og_images** — Добавлены 6 недостающих стран (Шри-Ланка, Черногория, Вьетнам, Грузия, Кипр, Оман)
23. **CAPTCHA** — Добавлена поддержка reCAPTCHA v2 на все 4 формы (base.html, home.html, destination-rich.html, contacts.html). Конфигурируется через RECAPTCHA_SITE_KEY в .env
24. **hreflang для country pages** — Проверено: hreflang корректен (была ложная тревога в аудите)
25. **Sticky CTA** — Исправлена навигация: base.html agent блок получил id="agent-form", article.html и destination-rich.html настраивают sticky_cta_target через Jinja2 переменную
26. **Copyright** — Сделан динамическим (current_year через date.today().year)
27. **Redirect page** — Добавлены canonical и noindex meta теги
28. **Copy-paste в template** — Создан централизованный DESTINATIONS_LIST в publisher.py, footer и формы используют Jinja2 циклы вместо хардкода
29. **FAQ статический** — generate_faq() теперь принимает country_slug/city_slug, загружает данные из COUNTRY_DATA, предоставляет персонализированные ответы для guide/hotels/flights/attractions/seasons
30. **RSS-фид** — Создан rss_generator.py, генерирует RSS 2.0 для RU и EN, автоматически встраивается в build процесс, добавлен `<link rel="alternate">` в base.html
31. **Error handling** — load_json() теперь обрабатывает corrupted JSON файлы с предупреждениями вместо краша
32. **Seasonal pages** — Создан seasonal_generator.py, 12 месяцев x 2 языка = 24 страницы "Куда поехать в [месяц]" с рекомендациями, погодой, ценами, советами. Добавлены в build процесс и sitemap

---

## Заметки

* Проект использует DeepSeek AI (через OpenAI-совместимый API) для генерации контента
* Travelpayouts marker: 736226
* Formspree ID: xnjyjnnd
* Email для связи: i@turkov-1.ru
* Валентина Туркова — реальный travel-агент, её имя сохраняется в контенте
* Фото агента хранятся в docs/assets/agent/ (webp)
