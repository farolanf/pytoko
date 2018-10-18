once(function bulmaInit () {
    
    utils.jqueryPlugin({
        modal: utils.jqueryPluginFactory(Modal, '__bulmaModal', 'show')
    })

    function Modal (el, options) {
        
        const $el = $(el)

        this.show = function show () {
            $el.addClass('is-active')
        }

        this.hide = function hide () {
            $el.removeClass('is-active')
        }

        $el.children('.modal-close, .modal-background').on('click', this.hide)
    }
})