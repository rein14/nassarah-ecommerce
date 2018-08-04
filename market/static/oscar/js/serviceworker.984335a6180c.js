// [Working example](/serviceworker-cookbook/offline-status/).


var CACHE_NAME = 'dependencies-cache';

// Files required to make this app work offline
var REQUIRED_FILES = [
'/static/oscar/css/css/vendor.min.css',
'/static/oscar/css/css/styles.min.css',
'/static/oscar/js/bootstrap-datetimepicker/bootstrap-datetimepicker.css',
'static/oscar/css/datetimepicker.css',
'/static/oscar/js/bootstrap-datetimepicker/bootstrap-datetimepicker.js',
'/static/oscar/js/bootstrap-datetimepicker/locales/bootstrap-datetimepicker.all.js',
'/static/oscar/js/oscar/ui.js',
'/static/oscar/js/jquery/jquery-1.9.1.min.js',
'/static/oscar/img/components/a3.jpg',
'/static/oscar/img/components/a2.jpg',
'/static/oscar/img/components/a1.jpg',
'/static/oscar/js/js/modernizr.min.js',
'/static/oscar/img/logo/logo.png',
'/static/oscar/js/js/vendor.min.js',
'/static/oscar/js/js/scripts.min.js',
'/static/oscar/js/js/card.min.js',
'/static/oscar/js/js/vendor.min.js',
'/static/oscar/img/shop/products/05.jpg',
'/static/oscar/img/top/s1.png',
'/static/oscar/img/top/w.png',
'/static/oscar/img/top/s3.png',
'/static/oscar/img/top/xxc.png',
'/static/oscar/img/components/x1.jpg',
'/static/oscar/img/components/x7.jpg',
'/static/oscar/img/components/c2.png',
'/static/oscar/img/components/c8.png',
'/static/oscar/img/components/c3.png',
'/static/oscar/img/components/c4.png',
'static/oscar/img/components/c5.png',
'/static/oscar/img/components/c6.png',
'/static/oscar/img/gallery/06.jpg',
'/static/oscar/img/gallery/05.jpg',
'/static/oscar/css/img/loading.gif',
'/static/oscar/css/img/loadin.gif',
'/static/oscar/img/account/default_profile.png',
'/static/oscar/css/fonts/feather-webfont.woff',
'/static/oscar/css/fonts/socicon.woff'
 

];

self.addEventListener('install', function(event) {
  // Perform install step:  loading each required file into cache
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        // Add all offline dependencies to the cache
        console.log('[install] Caches opened, adding all core components' +
          'to cache');
        return cache.addAll(REQUIRED_FILES);
      })
      .then(function() {
        console.log('[install] All required resources have been cached, ' +
          'we\'re good!');
        return self.skipWaiting();
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return the response from the cached version
        if (response) {
          console.log(
            '[fetch] Returning from ServiceWorker cache: ',
            event.request.url
          );
          return response;
        }

        // Not in cache - return the result from the live server
        // `fetch` is essentially a "fallback"
        console.log('[fetch] Returning from server: ', event.request.url);
        return fetch(event.request);
      }
    )
  );
});

self.addEventListener('activate', function(event) {
  console.log('[activate] Activating ServiceWorker!');

  // Calling claim() to force a "controllerchange" event on navigator.serviceWorker
  console.log('[activate] Claiming this ServiceWorker!');
  event.waitUntil(self.clients.claim());
});
