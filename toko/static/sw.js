
self.addEventListener('fetch', function (e) {
    e.respondWith(
        fetch(e.request).then(function (response) {
            if (e.request.url.startsWith('http')) {
                const responseClone = response.clone()
                caches.open('juwal').then(function (cache) {
                    cache.put(e.request, responseClone)
                })
            }
            return response
        }).catch(function () {
            return caches.match(e.request)
        })
    )
})