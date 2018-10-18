once(function imageUploads() {
    const containers = [document.querySelector('.image-uploads__container')]
    const drake = dragula(containers, {
        direction: 'horizontal',
    })
})