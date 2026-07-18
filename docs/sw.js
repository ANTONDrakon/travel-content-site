/*
 * TravelHub Service Worker
 * Provides offline caching and performance optimization
 */

const CACHE_NAME = 'travelhub-v1';
const STATIC_CACHE = 'travelhub-static-v1';
const IMAGE_CACHE = 'travelhub-images-v1';

// Assets to precache
const PRECACHE_URLS = [
  '/',
  '/en/index.html',
  '/ru/index.html',
  '/assets/styles.css',
  '/assets/tailwind.css',
  '/favicon.svg',
  '/404.html',
  '/404-ru.html'
];

// Install event - precache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== STATIC_CACHE && name !== IMAGE_CACHE)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip external requests (except images)
  if (url.origin !== location.origin) {
    // Cache images from external sources
    if (request.destination === 'image') {
      event.respondWith(cacheImage(request));
    }
    return;
  }

  // Handle different resource types
  if (request.destination === 'image') {
    event.respondWith(cacheImage(request));
  } else if (request.destination === 'style' || request.destination === 'script') {
    event.respondWith(cacheStatic(request));
  } else {
    event.respondWith(cachePage(request));
  }
});

// Cache static assets (CSS, JS)
async function cacheStatic(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    return new Response('Offline', { status: 503 });
  }
}

// Cache pages
async function cachePage(request) {
  // Try network first for HTML pages
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Fallback to cache
    const cached = await caches.match(request);
    if (cached) return cached;

    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      const offlinePage = await caches.match('/404.html');
      if (offlinePage) return offlinePage;
    }

    return new Response('Offline', { status: 503 });
  }
}

// Cache images
async function cacheImage(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(IMAGE_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Return placeholder for failed images
    return new Response(
      `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
        <rect fill="#e8e0d6" width="400" height="300"/>
        <text fill="#8a7e72" font-family="sans-serif" font-size="14" text-anchor="middle" x="200" y="150">Image offline</text>
      </svg>`,
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }
}
