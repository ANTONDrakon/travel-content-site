# MEMORY.md — TravelHub Project

## Current Status (2026-07-20)

### Homepage Redesign v5.0 — COMPLETED

**Full redesign from classic travel site to modern booking.com/Airbnb-level portal.**

#### New Design System
- Design tokens v5.0: CSS variables (--color-primary: #0066ff, gray-50…950 scale)
- Typography: all sizes in `rem` (h1: clamp(2.5rem, 6vw, 4rem), body: 1rem)
- BEM naming: `header--scrolled`, `lang-btn--active`, `section--alt`
- Shadow elevation system: xs → sm → md → lg → xl → card-hover
- Spacing scale: space-1 (0.25rem) through space-32 (8rem)

#### Homepage Sections (12 total)
1. **Hero** — 90vh, glass-morphism, 16 country pills, search
2. **Countries** — 3-col grid with images, flags, region/city counts
3. **Popular Destinations** — 8 compact horizontal cards (2-col)
4. **Popular Cities** — 8 cities in 4-col grid
5. **Best Hotels** — 6 cards from hotels.json (real data)
6. **Articles** — 3 blog-style cards (RU/EN/ES)
7. **Categories** — 8 tiles (beach, mountains, gastronomy, etc.)
8. **Why TravelHub** — 4 trust items (80+ countries, real prices, honest reviews, free help)
9. **Reviews** — 3 testimonial cards with avatars
10. **Agent Form** — Formspree with reCAPTCHA
11. **FAQ** — 5 questions (RU/EN/ES)
12. **Newsletter + RSS**

#### Header Redesign
- Sticky header with compact mode on scroll (4rem → 3.5rem)
- 6 nav items: Главная, Направления, Путеводители, Отели, О нас, Контакты
- Round flag language switcher (🇷🇺 🇬🇧 🇪🇸)
- Full-screen mobile menu with backdrop dimming
- Hamburger with aria-expanded toggle

#### Mobile Navigation
- Side panel (320px) with slide-in animation
- Dark backdrop (rgba(0,0,0,0.5))
- Close button (✕), TravelHub logo in header
- Language switcher at bottom of panel

### Architecture Fixes

#### Russian Regions
- `RUSSIA_STANDALONE_SLUGS` in publisher.py filters 9 standalone regions from homepage
- Regions (Baikal, Altai, Karelia, etc.) still exist as pages but not shown as countries
- `get_hotels_for_home()` loads 6 unique hotels with prices from data/hotels.json

#### New Countries
- Kazakhstan and Uzbekistan added to DESTINATIONS_LIST
- All country pages built with proper titles, regions, and navigation

#### Currency Localization
- RU: ₽ main + (USD in parens) — via `convert_prices_to_rub(lang="ru")`
- EN: $ USD only — no RUB, no parentheses
- ES: $ USD only — same as EN
- Hotel prices on EN homepage auto-converted from RUB to USD using exchange rate

#### Pluralization
- `ru_count()` macro added to base.html (available globally)
- destination-rich.html fixed: "1 город" instead of "1 городов"
- Correct Russian pluralization: 1 город, 2 города, 5 городов

#### Country Page Titles
- Fixed: "России → Россия", "Турции → Турция", "Таиланде → Таиланд"
- All 16 countries use nominative case in `<title>` and OG tags

### Image Optimization

#### Unique City Images
- 77 unique Unsplash images for 98 cities (was: 24 duplicates)
- Each city has a distinct WebP photo from Unsplash
- `CITY_IMAGES` dictionary completely rewritten with unique landmark photos

#### Region Images
- `REGION_IMAGES` dictionary: 70+ unique WebP images for all regions across 16 countries
- `get_region_image()` function in publisher.py, registered as Jinja2 global
- Region cards on destination pages now show photos, city-name tags, arrow indicators

#### Hotel Images
- `HOTEL_IMAGES` mapping: unique Unsplash WebP for each homepage hotel
- Aman Summer Palace, Rixos Premium, Hilton Hulhumale, etc. — each with distinct photo

#### WebP Format
- All Unsplash images use `?fm=webp` parameter (12 homepage images + 98 city images)
- Performance: ~50% size reduction vs JPEG

### Performance
- Google Fonts: async loading with `onload` pattern + `<noscript>` fallback
- CSS: `rel="preload"` for styles.css
- Unsplash: `rel="preconnect"` for images.unsplash.com
- All images: `loading="lazy"`, `width`/`height` attributes, `alt` text
- No unused CDN prefetch (removed dead cdn.tailwindcss.com dns-prefetch)
- `console.log` removed from production analytics.js

### UX Interaction Pass (Region Cards)
- Regions redesigned from text links to full Booking.com-style cards
- Each card: photo (52% ratio), city name tags (blue pills), city count, arrow indicator
- Full card clickable (not just text link)
- Hover: translateY(-4px), shadow boost, image zoom, arrow animation
- CSS: `.region-card`, `.region-card-img`, `.city-tag`, `.region-card-arrow`

### Template Changes
- `base.html`: `t()` and `ru_count()` macros, default `es_alt`/`ru_alt`/`en_alt` blocks
- `home.html`: 506 lines, 12 sections, `hide_agent=True`, `hide_back=True`
- `destination-rich.html`: region cards with images + city-tags, OG/title nominative case

### Build Process
- `build_all()`: copies `site/assets/` → `docs/assets/` via `shutil.copytree`
- 945 HTML files generated, 17.2% minification reduction
- Full pipeline: Tailwind → pages → sitemaps → RSS → seasonal → comparison → minification

### Accessibility
- All 41 homepage images: `alt`, `width`/`height`, `loading="lazy"`
- Semantic HTML: `<header>`, `<main>`, `<section>`, `<nav>`, `role=`, `aria-labelledby`
- Single `<h1>` per page, proper heading hierarchy
- `skip-link` for keyboard navigation
- `prefers-reduced-motion` support
- `aria-expanded` on hamburger, `aria-hidden` on decorative icons

### SEO
- `hreflang` for all 3 languages (ru/en/es)
- Schema.org: Organization, WebSite with SearchAction
- `sameAs` filled with Telegram/MAX links
- `availableLanguage: ["Russian", "English", "Spanish"]`
- OG tags, Twitter Cards, canonical URLs
- 455 URLs in sitemap-ru.xml, 455 in sitemap-en.xml

## Files Modified (key files)
- `publisher.py` — RUSSIA_STANDALONE_SLUGS, get_hotels_for_home(), get_region_image(), currency conversion
- `site/templates/home.html` — complete rewrite (506 lines)
- `site/templates/base.html` — header, macros, mobile nav, ES support
- `site/templates/destination-rich.html` — region cards, title fix, pluralization
- `site/assets/styles.css` — designsystem v5.0 (1260 lines)
- `site/assets/analytics.js` — console.log removed
- `config/destinations.py` — Kazakhstan, Uzbekistan added
- `vercel.json` — deployment config

## Deployment
- **Vercel:** https://travel-content-factory.vercel.app
- **GitHub Pages:** https://antondrakon.github.io/travel-content-site
- **GitHub:** https://github.com/ANTONDrakon/travel-content-site (master branch)
- Last commit: 56fdd358
