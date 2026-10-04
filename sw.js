/**
 * ZAYVORA Health OS™ — Enterprise Offline Service Worker (sw.js)
 * High-Reliability PWA Caching Strategy for Bedside & Mobile Clinics.
 */

const CACHE_NAME = 'zayvora-health-os-v15.2-live';
const OFFLINE_URL = './index.html';

const STATIC_PRECACHE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './tailwind.min.js',
  './js/zayvora-core.js',
  './js/zayvora-extensions.js'
];

// 1. Install: Precache Core App Shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ZAYVORA SW] Precaching application shell & offline assets...');
      return cache.addAll(STATIC_PRECACHE_ASSETS).catch((err) => {
        console.warn('[ZAYVORA SW] Precache non-critical item warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// 2. Activate: Clean up stale caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ZAYVORA SW] Purging legacy stale cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch: Dynamic Offline-First & Stale-While-Revalidate Routing
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET requests
  if (req.method !== 'GET') {
    return;
  }

  // HTML Navigation & Core App Shell: Network-First ALWAYS (with Cache Update)
  if (req.mode === 'navigate' || url.pathname === '/' || url.pathname.endsWith('/index.html')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(OFFLINE_URL).then((cached) => cached || fetch(req));
        })
    );
    return;
  }

  // JavaScript files: Network-First to guarantee fresh application logic
  if (url.pathname.endsWith('.js')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(req);
        })
    );
    return;
  }

  // API Calls: Network-First with Offline JSON Fallback
  if (url.pathname.startsWith('/api/v1/')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(req).then((cached) => {
            if (cached) return cached;
            return new Response(
              JSON.stringify({
                ok: true,
                offline_mode: true,
                message: 'ZAYVORA Mobile Clinic: Running in autonomous offline mode.',
                timestamp: new Date().toISOString()
              }),
              { headers: { 'Content-Type': 'application/json' } }
            );
          });
        })
    );
    return;
  }

  // Static Assets: Cache-First with Background Revalidation
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      if (cachedResponse) {
        // Revalidate in background
        fetch(req).then((freshResponse) => {
          if (freshResponse && freshResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(req, freshResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }
      return fetch(req).then((response) => {
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, responseToCache));
        }
        return response;
      });
    })
  );
});
