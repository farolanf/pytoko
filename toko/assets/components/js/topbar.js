once(function topBar () {

    $('#topbar').stickybar({ stickyClass: 'shadow-3' })

    $('.navbar-burger').on('click', function () {
        $(this).toggleClass('is-active')
        $($(this).attr('data-target')).toggleClass('is-active')
    })
})