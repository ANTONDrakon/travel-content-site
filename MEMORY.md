# MEMORY.md — Журнал проекта TravelHub

## ЭТАП 1: АУДИТ UI/UX

### Найденные проблемы

#### 1. CSS-система
| Проблема | Влияние | Исправление |
|----------|---------|-------------|
| Неполная палитра (5 цветов вместо 16) | Нет success/warning/danger/hover/active/disabled | Расширить до полной палитры |
| Нет spacing system | Случайные отступы | Создать 4-128px шкалу |
| Нет компонента Button | Разные размеры кнопок | Единый компонент sm/md/lg |
| Нет компонента Card | Разные стили карточек | Единый компонент card |
| Container 1120px | Слишком узкий для 1440px дизайна | Расширить до 1280px |
| Header 52px | Слишком маленький | Увеличить до 72px |

#### 2. Шаблоны
| Проблема | Влияние | Исправление |
|----------|---------|-------------|
| destination-rich.html: inline стили | Неочищенный код | Перенести в CSS |
| article.html: нет hero overlay | Плохая читаемость | Добавить overlay |
| seasonal.html: nav-pill устарел | Сломанные стили | Обновить |
| comparison.html: старые CSS-переменные | --teal вместо --blue | Обновить |

#### 3. Типографика
| Проблема | Влияние | Исправление |
|----------|---------|-------------|
| H1 64px на мобильных | Слишком большой | clamp() |
| Body 18px везде | Нет иерархии | Body L/M/S |
| Caption 15px | Маленький | Обновить |

#### 4. Сетка
| Проблема | Влияние | Исправление |
|----------|---------|-------------|
| 12 колонок нет | Не-standard | 12-колоночная сетка |
| Gutter 24px | Ок | Сохранить |
| Tablet 8 колонок | Нет | Добавить |

---

## ЭТАП 2: ДИЗАЙН-СИСТЕМА

### Палитра (16 цветов)
```
--primary: #0c2340      (navy)
--secondary: #1a5276    (ocean)
--accent: #0891b2       (teal)
--success: #10b981      (green)
--warning: #f59e0b      (amber)
--danger: #ef4444       (red)
--bg: #ffffff            (white)
--surface: #f8fafc      (light gray)
--card: #ffffff          (card bg)
--border: #e2e8f0       (border)
--muted: #94a3b8        (muted text)
--text: #0f172a         (primary text)
--text-secondary: #475569 (secondary text)
--text-muted: #94a3b8   (muted text)
--hover: #f1f5f9        (hover bg)
--active: #e2e8f0       (active bg)
--disabled: #cbd5e1     (disabled)
```

### Типографика
```
Display XL: 72px / 700 / -0.04em / 1.0
Display L: 56px / 700 / -0.035em / 1.05
H1: 48px / 700 / -0.03em / 1.1
H2: 36px / 700 / -0.025em / 1.15
H3: 28px / 600 / -0.02em / 1.2
H4: 22px / 600 / -0.015em / 1.3
Body L: 18px / 400 / 1.6
Body M: 16px / 400 / 1.6
Body S: 14px / 400 / 1.5
Caption: 12px / 500 / 1.4
Label: 11px / 600 / 1.3 / 0.06em
Button: 15px / 600 / 1.0
```

### Сетка
```
Desktop: 1440px / Content: 1280px / 12 cols / Gutter: 24px
Tablet: 8 cols
Mobile: 4 cols
```

### Spacing
```
4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128
```

### Radius
```
sm: 8px / md: 12px / lg: 16px / xl: 20px / 2xl: 24px / 3xl: 32px / full: 9999px
```

### Shadows
```
sm: 0 1px 2px rgba(0,0,0,0.05)
md: 0 4px 6px -1px rgba(0,0,0,0.07)
lg: 0 10px 15px -3px rgba(0,0,0,0.08)
xl: 0 20px 25px -5px rgba(0,0,0,0.1)
```

### Buttons
```
sm: h32 / 12px / radius 8px
md: h40 / 14px / radius 10px
lg: h48 / 16px / radius 12px
xl: h56 / 18px / radius 14px
```

---

## ЭТАП 3: ПЛАН РЕАЛИЗАЦИИ

### Этап 3.1: Design System CSS
- Расширить палитру до 16 цветов
- Добавить spacing, radius, shadow system
- Создать компоненты: Button, Card, Badge, Tag
- Обновить типографику

### Этап 3.2: Base Template
- Header 72px + blur
- Footer multi-column
- Newsletter

### Этап 3.3: Home Page
- Hero 70-80vh + search
- Country cards (large)
- City cards (compact)
- Collections (scroll)
- Articles (Medium-style)
- FAQ
- Newsletter

### Этап 3.4: Country Page
- Hero + info
- Weather
- Cities
- Articles
- FAQ

### Этап 3.5: Article Page
- Hero
- TOC
- Content
- Related
- FAQ

### Этап 3.6: Mobile Optimization
- 4-column grid
- Touch targets
- Sticky CTA

---

## Дата: 2026-07-18
