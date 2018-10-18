once(function imageUploads () {
    
    const containers = [document.querySelector('.image-uploads__container')]
    
    const drake = dragula(containers, {
        direction: 'horizontal',
    })

    $('.image-upload').each(function (i, el) {
        new ImageUpload(el)
    })

    function ImageUpload (el) {

        $('.image-upload__crop', el).on('click', function () {
            
            const $modal = $('.image-uploads__cropper-modal')
            const $img = $('img', el)
            let cropper

            $modal.modal({
                onShow () {
                    cropper = initCropper()
                },
                onHide () {
                    if (cropper) {
                        cropper.destroy()
                        cropper = null
                    }
                }
            })
            
            function initCropper () {
                const img = $modal.find('img').get(0)
                img.src = $img.attr('src')
                return new Cropper(img, {
                    rotatable: true,
                    viewMode: 2
                })
            }

            $modal.find('.button.rotate-left')
                .off('click')
                .on('click', function () {
                    cropper.rotate(-90)
                })

            $modal.find('.button.rotate-right')
                .off('click')
                .on('click', function () {
                    cropper.rotate(90)
                })
        })
    }
})