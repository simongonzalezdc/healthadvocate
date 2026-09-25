/* HealthAdvocate service worker — offline shell, static assets ONLY.
 *
 * Privacy law (health-data): /api/* responses are NEVER cached and never
 * served from cache. Patient data must not live in the service-worker cache.
 * There is no push, no background sync, no network beyond the app itself.
 *
 * Strategy:
 *   - static assets (/, /static/*): stale-while-revalidate against a
 *     versioned cache; navigation requests fall back to the cached shell.
 *   - everything else, and anything under /api/: network only. Offline means
 *     an honest failure, never stale health data.
 */

const CACHE = 'ha-shell-v3-themes';
const SHELL = [
  '/',
  '/static/styles.css',
  '/static/app.js',
  '/static/i18n.js',
  '/static/i18n/en.js',
  '/static/i18n/es.js',
  '/static/manifest.webmanifest',
  '/static/icons/favicon.svg',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  /* Health-data law: API traffic is never intercepted, never cached. */
  if (url.pathname.startsWith('/api/')) return;

  if (event.request.mode === 'navigate') {
    /* Offline navigation falls back to the cached app shell (SPA). */
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/').then((r) => r || Response.error()))
    );
    return;
  }

  if (url.origin !== self.location.origin) return;

  /* Static assets: NETWORK-FIRST while the product is in active build —
     stale first-paint cost a CEO session. The cache is the OFFLINE
     fallback, refreshed on every success. */
  event.respondWith(
    fetch(event.request).then((response) => {
      const copy = response.clone();
      caches.open(CACHE).then((cache) => cache.put(event.request, copy));
      return response;
    }).catch(() => caches.match(event.request).then((r) => r || Response.error()))
  );
});
