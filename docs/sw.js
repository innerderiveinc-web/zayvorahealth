/**
 * ZAYVORA Health OS™ — Enterprise Offline Service Worker (sw.js)
 * High-Reliability PWA Caching Strategy for Bedside & Mobile Clinics.
 */

const CACHE_NAME = 'zayvora-health-os-v8.0-clean';
const OFFLINE_URL = './index.html';

const STATIC_PRECACHE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './apps/web/public/zayvora-logo.png'
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
            console.log('[ZAYVORA SW] Removing legacy cache:', key);
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

  // HTML Navigation: Network-First with Offline Cache Fallback
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() => {
        return caches.match(OFFLINE_URL).then((cached) => {
          return cached || fetch(req);
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
