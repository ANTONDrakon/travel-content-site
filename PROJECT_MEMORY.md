# PROJECT_MEMORY.md — AI Travel Content Factory

## Общая цель проекта

Автоматическая система генерации туристического контента с SEO-оптимизацией и партнёрскими ссылками Travelpayouts. Цель — коммерческий туристический сайт, приносящий доход через партнёрские программы и заявки на подбор туров.

**Стек:** Python, Jinja2, Tailwind CSS (CDN), DeepSeek AI API, GitHub Pages  
**Языки:** RU + EN (двуязычный)  
**Монетизация:** Travelpayouts (Aviasales, Hotellook, Booking, Agoda и др.) + Formspree (заявки на туры)

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

---

## Найденные проблемы

### КРИТИЧЕСКИЕ (P0)

1. **robots.txt — case inconsistency**: В `docs/robots.txt` и `docs/sitemap.xml` URL содержит `ANTONDrakon` (ALL CAPS), а в `.env.example` и `publisher.py` — `antondrakon` (lowercase). GitHub Pages URL-адреса case-sensitive → страницы могут не индексироваться.

2. **Schema.org dates hardcoded**: В `seo_optimizer.py:69-70` даты `datePublished: "2026-01-15"` и `dateModified: "2026-06-01"` захардкожены для ВСЕХ статей. Google может понизить ранжирование за неактуальные даты.

3. **Нет 404 страницы**: Если пользователь попадает на несуществующую страницу — стандартная ошибка GitHub Pages без навигации.

4. **Нет файла .env**: Без переменных окружения проект не работает. `.env.example` содержит ключи API, но нет инструкции по безопасному хранению.

5. **megatec_output.html** — посторонний файл (страница ошибки .NET сайта) в корне проекта. Не относится к проекту.

### ВАЖНЫЕ (P1)

6. **CDN Tailwind CSS**: Используется `cdn.tailwindcss.com` (dev-скрипт, не для продакшена). Нужно собирать CSS или использовать CDN-билд.

7. **Нет lazy loading для hero-изображений**: Все hero-секции загружаются сразу, что замедляет FCP.

8. **Formspree без CAPTCHA**: Формы заявок не защищены от спама — могут забиваться мусорными заявками.

9. **Мета-теги AI-контента**: `<meta name="ai-content-type">`, `<meta name="ai-audience">`, `<meta name="ai-tone">`, `<meta name="ai-topics">`, `<meta name="ai-verification">` — нет стандартов для этих тегов. Google их игнорирует, но они выглядят нестандартно.

10. **Нет OpenGraph image для всех стран**: В `publisher.py` `COUNTRY_IMAGES` содержит только 7 стран, хотя проект поддерживает 13. Для стран без OG-image будет fallback на generic.

11. **CITY_IMAGES не покрывают все города**: Словарь `CITY_IMAGES` содержит ~35 городов, но проект имеет ~60. Города без изображений получают generic fallback.

12. **Нет hreflang для country index pages**: В шаблоне `destination-rich.html` hreflang ссылки ведут на `index.html`, но canonical — на `/{lang}/{country}/index.html`.

13. **Форма в footer не привязана к #agent-form**: Sticky CTA ведёт на `#agent-form`, но на страницах статей этот ID может отсутствовать.

14. **Нет Breadcrumb Schema для country pages**: BreadcrumbList генерируется только для статей, не для страниц стран.

### СРЕДНИЕ (P2)

15. **Дублирование CSS**: Все стили в `base.html` (537 строк) — нет внешнего CSS-файла, нет кэширования браузером.

16. **Swiper.js подключается, но не используется**: В `base.html` подключён `swiper-bundle.min.css` и `swiper-bundle.min.js`, но нигде не применяется.

17. **Нет аналитики**: Нет Яндекс.Метрика, Google Analytics, или другой системы аналитики.

18. **Нет favicon**: Нет иконки для сайта.

19. **Нет Service Worker / PWA**: Нет офлайн-поддержки.

20. **Copyright 2026**: Уже захардкожен — через год потребует обновления.

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

31. **Нет email-подписки**: Нет лид-магнита.

32. **Нет seasonal pages**: Нет отдельных страниц "Куда поехать в июле".

33. **Нет сравнения направлений**: Нет страниц "Турция vs Египет".

34. **Нет блога**: Только сгенерированные статьи.

35. **Нет RSS-фида**: Для подписчиков.

36. **Нет страницы "Партнёрам"**: Нет информации для потенциальных партнёров.

37. **Нет breadcrumbs в JSON-LD для country pages**: Только для статей.

38. **Нет i18n для статических элементов**: "TravelHub", "Expert guide" и т.д. захардкожены.

39. **Нет error handling в publisher.py**: Если JSON-файл повреждён — краш без информации.

40. **Нет тестов**: Только `photo_pipeline/tests/test_verifier.py`.

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

1. Исправить критические проблемы (P0)
2. Исправить важные проблемы (P1)
3. Добавить российские направления
4. Добавить международные направления
5. Улучшить UX/UI
6. Добавить аналитику
7. Оптимизировать производительность

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

---

## Заметки

* Проект использует DeepSeek AI (через OpenAI-совместимый API) для генерации контента
* Travelpayouts marker: 736226
* Formspree ID: xnjyjnnd
* Email для связи: i@turkov-1.ru
* Валентина Туркова — реальный travel-агент, её имя сохраняется в контенте
* Фото агента хранятся в docs/assets/agent/ (webp)
