/*
 * TravelHub Analytics Module
 * Handles Yandex.Metrika, Google Analytics, and custom event tracking
 */

// Configuration
const ANALYTICS_CONFIG = {
    yandexMetrikaId: null, // Set your Yandex.Metrika ID
    googleAnalyticsId: null, // Set your GA4 Measurement ID (G-XXXXXXXXXX)
    enabled: true
};

// Initialize analytics
function initAnalytics() {
    if (!ANALYTICS_CONFIG.enabled) return;

    // Load Yandex.Metrika
    if (ANALYTICS_CONFIG.yandexMetrikaId) {
        loadYandexMetrika(ANALYTICS_CONFIG.yandexMetrikaId);
    }

    // Load Google Analytics
    if (ANALYTICS_CONFIG.googleAnalyticsId) {
        loadGoogleAnalytics(ANALYTICS_CONFIG.googleAnalyticsId);
    }

    // Setup event tracking
    setupEventTracking();
}

// Yandex.Metrika
function loadYandexMetrika(id) {
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();
    for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

    ym(id, "init", {
        ssr: true,
        webvisor: true,
        clickmap: true,
        ecommerce: "dataLayer",
        accurateTrackBounce: true,
        trackLinks: true
    });
}

// Google Analytics
function loadGoogleAnalytics(id) {
    // gtag.js
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', id, {
        page_title: document.title,
        page_location: window.location.href
    });
}

// Event tracking setup
function setupEventTracking() {
    // Track affiliate link clicks
    document.addEventListener('click', function(e) {
        var link = e.target.closest('a[href*="tp.media"], a[href*="travelpayouts"], a.partner-link');
        if (link) {
            trackEvent('affiliate_click', {
                url: link.href,
                text: link.textContent.trim(),
                page: window.location.pathname
            });
        }
    });

    // Track form submissions
    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (form.action && form.action.includes('formspree')) {
            trackEvent('form_submit', {
                form_id: form.id || 'unknown',
                page: window.location.pathname
            });
        }
    });

    // Track CTA button clicks
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.btn-cta, .partner-btn');
        if (btn) {
            trackEvent('cta_click', {
                text: btn.textContent.trim(),
                href: btn.href || '',
                page: window.location.pathname
            });
        }
    });

    // Track scroll depth
    var maxScroll = 0;
    window.addEventListener('scroll', function() {
        var scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        if (scrollPercent > maxScroll && scrollPercent % 25 === 0) {
            maxScroll = scrollPercent;
            trackEvent('scroll_depth', {
                percent: scrollPercent,
                page: window.location.pathname
            });
        }
    });

    // Track time on page
    var startTime = Date.now();
    window.addEventListener('beforeunload', function() {
        var timeSpent = Math.round((Date.now() - startTime) / 1000);
        trackEvent('time_on_page', {
            seconds: timeSpent,
            page: window.location.pathname
        });
    });
}

// Track custom event
function trackEvent(eventName, params) {
    // Yandex.Metrika
    if (typeof ym !== 'undefined') {
        ym(ANALYTICS_CONFIG.yandexMetrikaId, 'reachGoal', eventName, params);
    }

    // Google Analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, params);
    }

    // Console log for debugging
    console.log('Analytics:', eventName, params);
}

// Track page view (for SPA)
function trackPageView(url, title) {
    // Yandex.Metrika
    if (typeof ym !== 'undefined') {
        ym(ANALYTICS_CONFIG.yandexMetrikaId, 'hit', url, {
            title: title,
            referrer: document.referrer
        });
    }

    // Google Analytics
    if (typeof gtag !== 'undefined') {
        gtag('config', ANALYTICS_CONFIG.googleAnalyticsId, {
            page_path: url,
            page_title: title
        });
    }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnalytics);
} else {
    initAnalytics();
}

// Export for use in other scripts
window.TravelHubAnalytics = {
    trackEvent: trackEvent,
    trackPageView: trackPageView,
    config: ANALYTICS_CONFIG
};
