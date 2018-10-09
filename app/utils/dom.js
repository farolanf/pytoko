
export function scrollToError () {
    const target = $('.field').toArray().find(el => $('.is-danger', el).length)
    if (!target) return
    $([document.documentElement, document.body]).animate({
        scrollTop: $(target).offset().top - 60
    })
}