# Деплой TravelHub на GitHub Pages

## Быстрый деплой

### 1. Подготовка

```bash
# Установить зависимости
pip install -r requirements.txt
npm install

# Настроить .env файл
cp .env.example .env
# Заполните API ключи
```

### 2. Генерация контента (если нужно)

```bash
# Сгенерировать контент для всех направлений
python main.py generate --lang both

# Или для конкретной страны
python main.py generate --country turkey --lang both
```

### 3. Сборка сайта

```bash
# Полная сборка (Tailwind CSS + HTML + минификация + sitemap)
python main.py build
```

### 4. Публикация на GitHub

```bash
# Инициализировать git (если ещё не)
git init
git add .
git commit -m "Initial commit"

# Подключить репозиторий
git remote add origin https://github.com/ANTONDrakon/travel-content-site.git
git branch -M main
git push -u origin main
```

### 5. Настройка GitHub Pages

1. Перейти в **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **/docs**
4. Нажать **Save**

Сайт будет доступен по адресу:
`https://antondrakon.github.io/travel-content-site`

---

## Развёртывание на других хостингах

### Netlify

1. Подключить GitHub репозиторий
2. Build command: `python main.py build`
3. Publish directory: `docs`
4. Файл `netlify.toml` уже настроен

### Vercel

1. Подключить GitHub репозиторий
2. Framework: **Other**
3. Build command: `python main.py build`
4. Output directory: `docs`

### Self-hosted (Apache/Nginx)

1. Скопировать содержимое `docs/` на сервер
2. Настроить `.htaccess` (уже создан)
3. Включить mod_rewrite для Apache

---

## Проверка после деплоя

### Что проверить

- [ ] Главная страница загружается
- [ ] Переключение языков работает (EN/RU)
- [ ] Навигация работает
- [ ] Формы отправляются
- [ ] Изображения загружаются
- [ ] Мобильная версия работает
- [ ] SEO-теги отображаются (inspect element)
- [ ] Schema.org валиден (Google Rich Results Test)
- [ ] Sitemap доступен: `/sitemap.xml`
- [ ] Robots.txt доступен: `/robots.txt`

### Инструменты для проверки

- **Google Search Console**: https://search.google.com/search-console
- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **PageSpeed Insights**: https://pagespeed.web.dev/
- **Mobile-Friendly Test**: https://search.google.com/test/mobile-friendly

---

## Генерация контента для новых направлений

Новые направления (Россия, Байкал и др.) были добавлены в конфигурацию, но контент ещё не сгенерирован. Для генерации:

```bash
# Сгенерировать контент для России
python main.py generate --country russia --lang both

# Сгенерировать контент для Байкала
python main.py generate --country baikal --lang both

# Сгенерировать всё
python main.py generate --lang both
```

**Важно:** Для генерации контента необходим API ключ DeepSeek.

---

## Мониторинг

### Аналитика

1. Подключить Яндекс.Метрику
2. Подключить Google Analytics
3. Настроить цели (отправка формы, клик по партнёрской ссылке)

### Поисковая оптимизация

1. Добавить сайт в Google Search Console
2. Добавить сайт в Яндекс.Вебмастер
3. Отправить sitemap: `https://antondrakon.github.io/travel-content-site/sitemap.xml`

---

## Частые проблемы

### Tailwind CSS не собирается

```bash
# Переустановить зависимости
rm -rf node_modules
npm install
npm run tailwind:build
```

### Ошибки в шаблонах

Проверить синтаксис Jinja2 в файлах `site/templates/`.

### Формы не работают

Убедиться, что Formspree ID правильный: `xnjyjnnd`

### Партнёрские ссылки не работают

Проверить Travelpayouts маркер в `.env`: `736226`
