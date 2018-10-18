
const utils = {
    
    scrollToError () {
        const target = $('.field').toArray().find(el => $('.is-danger', el).length)
        if (!target) return
        this.scrollTo(target, -60)
        $('input, textarea, select', target).focus()
    },

    scrollTo (target, offset = 0) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(target).offset().top + offset
        })
    }
}