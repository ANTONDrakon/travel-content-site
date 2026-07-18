/*
 * TravelHub Performance Monitor
 * Tracks Core Web Vitals and performance metrics
 */

(function() {
    'use strict';

    // Performance metrics storage
    var metrics = {
        fcp: null,
        lcp: null,
        cls: null,
        ttfb: null,
        fid: null
    };

    // Track First Contentful Paint (FCP)
    function trackFCP() {
        var observer = new PerformanceObserver(function(entryList) {
            var entries = entryList.getEntries();
            if (entries.length > 0) {
                metrics.fcp = Math.round(entries[0].startTime);
                console.log('FCP:', metrics.fcp + 'ms');
            }
        });
        observer.observe({ type: 'paint', buffered: true });
    }

    // Track Largest Contentful Paint (LCP)
    function trackLCP() {
        var observer = new PerformanceObserver(function(entryList) {
            var entries = entryList.getEntries();
            var lastEntry = entries[entries.length - 1];
            metrics.lcp = Math.round(lastEntry.startTime);
            console.log('LCP:', metrics.lcp + 'ms');
        });
        observer.observe({ type: 'largest-contentful-paint', buffered: true });
    }

    // Track Cumulative Layout Shift (CLS)
    function trackCLS() {
        var observer = new PerformanceObserver(function(entryList) {
            var entries = entryList.getEntries();
            var clsValue = 0;
            entries.forEach(function(entry) {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                }
            });
            metrics.cls = clsValue.toFixed(3);
            console.log('CLS:', metrics.cls);
        });
        observer.observe({ type: 'layout-shift', buffered: true });
    }

    // Track Time to First Byte (TTFB)
    function trackTTFB() {
        var navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            metrics.ttfb = Math.round(navigation.responseStart - navigation.requestStart);
            console.log('TTFB:', metrics.ttfb + 'ms');
        }
    }

    // Track First Input Delay (FID)
    function trackFID() {
        var observer = new PerformanceObserver(function(entryList) {
            var entries = entryList.getEntries();
            entries.forEach(function(entry) {
                metrics.fid = Math.round(entry.processingStart - entry.startTime);
                console.log('FID:', metrics.fid + 'ms');
            });
        });
        observer.observe({ type: 'first-input', buffered: true });
    }

    // Send metrics to analytics
    function sendMetrics() {
        if (window.TravelHubAnalytics && window.TravelHubAnalytics.trackEvent) {
            window.TravelHubAnalytics.trackEvent('performance_metrics', metrics);
        }
    }

    // Initialize monitoring
    function init() {
        trackFCP();
        trackLCP();
        trackCLS();
        trackTTFB();
        trackFID();

        // Send metrics after page load
        window.addEventListener('load', function() {
            setTimeout(sendMetrics, 1000);
        });
    }

    // Start monitoring
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
