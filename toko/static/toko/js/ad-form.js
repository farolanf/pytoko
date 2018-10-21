once(function adForm () {
    
    const $form = $('#ad-form')

    const tokenField = 'csrfmiddlewaretoken'
    const csrfToken = $(`[name="${tokenField}"]`, $form).val()
    
    $form.on('submit', function (e) {
        e.preventDefault()

        const imgs = $('.image-upload img', $form).toArray()

        fetchImageBlobs(imgs)
            .then(blobs => {
                const fd = new FormData()
                fd.append(tokenField, csrfToken)
                blobs.forEach((blob, i) => {
                    if (!blob) return
                    const name = $(imgs[i]).attr('data-name')
                    fd.append(`files[${i}]`, blob, name)
                })
                $.ajax({
                    url: '/files/new/',
                    method: 'POST',
                    processData: false,
                    contentType: false,
                    data: fd,
                })
            })
    })

    function fetchImageBlobs(imgs) {
        return Promise.all(
            imgs.map(img => img.src ? blobFromDataUrl(img.src) : null)
        )
    }

    function blobFromDataUrl(dataUrl) {
        return fetch(dataUrl).then(r => r.blob())
    }
})