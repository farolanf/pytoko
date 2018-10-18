once(function bulmaInit () {
    
    utils.jqueryPlugin({
        modal: utils.jqueryPluginFactory(Modal, '__bulmaModal', 'show')
    })

    function Modal (el, options) {
        
        const $el = $(el)

        this.setOptions = function setOptions (opts) {
            options = opts
        }

        this.show = function show () {
            options.onShow && options.onShow()
            $el.addClass('is-active')
        }

        this.hide = function hide () {
            options.onHide && options.onHide()
            $el.removeClass('is-active')
        }

        $el.find('.modal-close, .modal-background, .modal-card-head .delete, .close-button')
            .on('click', this.hide)
    }
})