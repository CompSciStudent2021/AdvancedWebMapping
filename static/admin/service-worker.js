const CACHE_NAME = 'gym-locator-cache-v1';
const urlsToCache = [
  '/static/admin/css/base.css',
  '/static/admin/js/core.js',
  '/static/admin/img/icon-192x192.png',
  '/static/admin/img/icon-512x512.png'
];

// Install service worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.all(
        urlsToCache.map((url) =>
          fetch(url)
            .then((response) => {
              if (!response.ok) {
                throw new Error(`Failed to fetch ${url}, status: ${response.status}`);
              }
              return cache.put(url, response);
            })
            .catch((err) => {
              console.error(`Failed to cache ${url}:`, err);
            })
        )
      );
    })
  );
});

// Fetch resources
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// Activate service worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
