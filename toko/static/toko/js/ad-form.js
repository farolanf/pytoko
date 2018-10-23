once(function adForm () {
    
    const $form = $('#ad-form')

    const tokenField = 'csrfmiddlewaretoken'
    const csrfToken = $(`[name="${tokenField}"]`, $form).val()
    
    let processed = false

    $form.on('submit', function (e) {
        if (processed) return
        e.preventDefault()
        processFiles().then(result => {

            if (result) {
                // save new ids 
                result.data.add && result.data.add.forEach((item, i) => {
                    result.post.add[i].id = item.id
                })
            }

            processed = true

            // wait for vue to render the ids
            setTimeout(() => {
                $form.submit()
            })
        })        
    })

    function processFiles () {

        const post = {
            del: [],
            add: [],
            update: [],
        }

        DATA.imageUploads.forEach((item, i) => {
            if (isDeleted(item)) {
                post.del.push(item)
            } else if (isAdded(item)) {
                post.add.push(item)
            } else if (isChanged(item)) {
                post.update.push(item)
            }
        })

        if (!post.del.length && !post.add.length && !post.update.length) {
            return Promise.resolve()
        }

        return Promise.all([
            Promise.all(generateBlobs(post.del)),
            Promise.all(generateBlobs(post.add)),
            Promise.all(generateBlobs(post.update)),
        ]).then(results => {
            post.del = results[0]
            post.add = results[1]
            post.update = results[2]
            return postData(post)
        })
    }

    function isDeleted(item) {
        return item.originalFile && !item.file
    }

    function isAdded(item) {
        return !item.originalFile && item.file
    }

    function isChanged(item) {
        return item.file !== item.originalFile
    }

    function postData(post) {
        const fd = new FormData()
        fd.append(tokenField, csrfToken)

        post.del.forEach((item, i) => {
            fd.append(`del[${i}]`, item.id)
        })

        post.add.forEach((item, i) => {
            fd.append(`add[${i}]`, item.blob, item.name)
        })

        post.update.forEach((item, i) => {
            fd.append(`update[${i}]id`, item.id)
            fd.append(`update[${i}]file`, item.blob)
        })

        return $.ajax({
            url: '/files/process/',
            method: 'POST',
            processData: false,
            contentType: false,
            data: fd,
        }).then(data => ({ data, post }))
    }

    function generateBlobs(items) {
        return items.map(item => 
            blobFromDataUrl(item.file).then(blob => {
                item.blob = blob
                return item
            })
        )
    }
    
    function blobFromDataUrl(dataUrl) {
        return fetch(dataUrl).then(r => r.blob())
    }
})