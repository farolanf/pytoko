once(function adForm () {
    
    const $form = $('#ad-form')

    const tokenField = 'csrfmiddlewaretoken'
    const csrfToken = $(`[name="${tokenField}"]`, $form).val()
    
    let uploaded = false

    $form.on('submit', function (e) {
        if (uploaded) return
        e.preventDefault()
        uploadFiles().then(resp => {
            if (resp) {
                $('[name="images[]"]').each((i, el) => {
                    if (i >= resp.files.length) return
                    el.name = `images[${i}]`;
                    el.value = resp.files[i].id
                })
            }
            uploaded = true
            $form.submit()
        })        
    })

    function uploadFiles () {
        const imgs = $('.image-upload img', $form).toArray()

        return fetchImageBlobs(imgs).then(blobs => {
            const fd = new FormData()
            fd.append(tokenField, csrfToken)

            let count = 0
            blobs.forEach((blob, i) => {
                if (!blob) return
                count++
                const name = $(imgs[i]).attr('data-name')
                fd.append(`files[${i}]`, blob, name)
            })
            if (!count) return

            return $.ajax({
                url: '/files/new/',
                method: 'POST',
                processData: false,
                contentType: false,
                data: fd,
            })
        })
    }

    function fetchImageBlobs(imgs) {
        return Promise.all(
            imgs.map(img => img.src ? blobFromDataUrl(img.src) : null)
        )
    }

    function blobFromDataUrl(dataUrl) {
        return fetch(dataUrl).then(r => r.blob())
    }
})