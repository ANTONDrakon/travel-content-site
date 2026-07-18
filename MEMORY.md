# MEMORY.md — Журнал проекта TravelHub

## Общая цель проекта

Автоматическая система генерации туристического контента с SEO-оптимизацией и партнёрскими ссылками Travelpayouts. Двуязычный (RU + EN) статический сайт для GitHub Pages / Netlify.

---

## Статус задач

| Приоритет | Всего | Исполнено | Остаток |
|-----------|-------|-----------|---------|
| P0 | 7 | 7 | 0 |
| P1 | 9 | 9 | 0 |
| P2 | 9 | 9 | 0 |
| P3 | 9 | 9 | 0 |
| **Итого** | **34** | **34** | **0** |

---

## Выполнено (сводка за все сессии)

### P0 — Критические
1. robots.txt — исправлен регистр URL
2. Schema.org — даты динамические (date.today())
3. 404 страница — создана
4. article.html — published_time/modified_time динамические
5. publisher.py — lazy loading для exchange rates
6. publisher.py — bare except заменены на конкретные
7. publisher.py — опечатка "cănзуется" → "требуется"

### P1 — Важные
8. reCAPTCHA v2 добавлена на все 4 формы
9. CITY_IMAGES — добавлены все ~80 городов
10. og_images — добавлены все 21 страна
11. base.html footer — все 22 направления
12. contacts.html — WhatsApp, исправлена Telegram
13. Sticky CTA — настроен через sticky_cta_target
14. hreflang — проверено, корректен
15. Breadcrumb Schema — добавлен для country pages

### P2 — Средние
16. Copyright — динамический (current_year)
17. Redirect page — canonical + noindex
18. Copy-paste — централизованный DESTINATIONS_LIST
19. FAQ — динамический с данными из COUNTRY_DATA
20. CSS вынесен в styles.css
21. Analytics.js создан
22. Service Worker создан
23. Favicon добавлен

### P3 — Низкие
24. RSS-фид — rss_generator.py (RU + EN)
25. Seasonal pages — 12 месяцев x 2 языка = 24 страницы
26. Error handling — load_json() с обработкой ошибок
27. Сравнение направлений — comparison_generator.py (3 сравнения x 2 языка = 6 страниц)
28. Email-подписка — Brevo интеграция, форма в footer и homepage

---

## Оставшиеся задачи

Все P0, P1, P2 и P3 задачи выполнены.

### Возможные улучшения (не в приоритете)
- Добавить больше сравнений направлений
- Расширить seasonal pages более детальными данными
- Добавить больше городов в CONTENT_TYPES
- Интеграция с Яндекс.Метрикой (нужен ID)
- Добавить更多 страниц сравнений

---

## Ключевые файлы

| Файл | Назначение |
|------|------------|
| `main.py` | CLI: generate, build, all, list |
| `publisher.py` | Сборка HTML (Jinja2, ~1100 строк) |
| `sitemap_generator.py` | Генерация sitemap.xml |
| `rss_generator.py` | Генерация RSS 2.0 |
| `seasonal_generator.py` | Генерация seasonal pages |
| `comparison_generator.py` | Генерация comparison pages |
| `config/destinations.py` | 21 страна, ~80 городов |
| `config/country_data.py` | Подробные данные по странам |
| `config/prompts.py` | Промпты для AI |
| `config/affiliates.py` | Партнёрские ссылки |
| `agents/seo_optimizer.py` | SEO, Schema.org, FAQ |
| `agents/content_writer.py` | DeepSeek API |
| `agents/image_injector.py` | Фото отелей |
| `site/templates/` | Jinja2 шаблоны |

---

## Переменные окружения (.env)

```
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
TRAVELPAYOUTS_MARKER=736226
SITE_URL=https://antondrakon.github.io/travel-content-site
RECAPTCHA_SITE_KEY=...  # Для форм
ANALYTICS_ENABLED=true
YANDEX_METRIKA_ID=...
GOOGLE_ANALYTICS_ID=G-...
```

---

## Команды

```bash
# Генерация контента
python main.py generate --country turkey --lang both
python main.py generate --lang both  # всё

# Сборка сайта
python main.py build  # HTML + Tailwind + sitemap + RSS + seasonal + comparisons

# Полная сборка
python main.py all  # generate + build
```

---

## Дата последнего обновления

2026-07-18
