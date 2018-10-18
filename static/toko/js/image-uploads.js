once(function imageUploads () {
    
    const containers = [document.querySelector('.image-uploads__container')]
    
    const drake = dragula(containers, {
        direction: 'horizontal',
    })

    $('.image-upload').each(function (i, el) {
        new ImageUpload(el)
    })

    function ImageUpload (el) {

        let cropper

        const $img = $('img', el)

        $('.image-upload__crop', el).on('click', function () {
            showCropperModal()
        })

    }

    function showCropperModal () {
        const $modal = $('.image-uploads__cropper-modal').modal()

        // cropper = new Cropper($img.get(0), {
        //     rotatable: true
        // })
    }
})