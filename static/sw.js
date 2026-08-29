self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('espace-zen-store').then((cache) => {
      return cache.addAll([
        '/',
        '/static/css/style.css'
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});