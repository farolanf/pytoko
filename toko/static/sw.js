
self.addEventListener('fetch', function (e) {
    if (! (e.request.method === 'GET' && e.request.url.startsWith('http'))) {
        return
    }
    e.respondWith(
        fetch(e.request).then(function (response) {
            const responseClone = response.clone()
            caches.open('get').then(function (cache) {
                cache.put(e.request, responseClone)
            })
            return response
        }).catch(function () {
            return caches.match(e.request)
        })
    )
})