const CACHE_NAME = 'counter-app-v1';
const urlsToCache = [
  './',
  './index.html',
  './main.py',
  './pyscript.json',
  './templates/counter.tpl',
  './templates/button.tpl',
  'https://cdn.tailwindcss.com',
  'https://pyscript.net/releases/2025.8.1/core.css',
  'https://pyscript.net/releases/2025.8.1/core.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      }
    )
  );
});