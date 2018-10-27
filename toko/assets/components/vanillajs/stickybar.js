once(function stickybar () {
    /**
     * Set sticky class of a navbar when it's in sticky state.
     */

    utils.jqueryPlugin({
        stickybar: utils.jqueryPluginFactory(Stickybar, '__stickybar')
    })

    function Stickybar(el, options) {

        options = Object.assign({}, {
            stickyClass: 'stickybar--sticky'
        }, options)

        // observed element
        const target = document.createElement('div')
        target.style = 'position: absolute; width: 100%; top: 0; height: 8px'
        document.body.insertBefore(target, el.nextSibling)

        // counter toggle
        el.classList.toggle(options.stickyClass)

        const observer = new IntersectionObserver(() => {
            el.classList.toggle(options.stickyClass)
        })
        
        observer.observe(target)
    }
})