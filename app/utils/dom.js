
export function scrollToError () {
    const target = $('.field').toArray().find(el => $('.is-danger', el).length)
    if (!target) return
    scrollTo(target, -60)
}

export function scrollTo (target, offset = 0) {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(target).offset().top + offset
    })
}