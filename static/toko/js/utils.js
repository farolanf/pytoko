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
    },

    jqueryPlugin (pluginObj) {
        $.fn.extend(pluginObj)
    },

    /**
     * Instantiate constructor  
     * 
     * @param {function} constructor The constructor
     * @param {string} instanceName Attribute name on the element to store the instance
     * @param {string} defaultMethod Default method to be called on invocation
     */
    jqueryPluginFactory (constructor, instanceName, defaultMethod) {
        
        return function () {
        
            const method = arguments.length ? arguments[0] : undefined
            const args = Array.prototype.slice.call(arguments, 1)
        
            return this.each(function (i, el) {
                invoke(el, method, args)
            })
        }

        function invoke (el, method, args) {

            const options = typeof method === 'object' ? method : undefined

            if (!el[instanceName]) {
                el[instanceName] = new constructor(el, options)
                call(el[instanceName], method)
                return
            }

            const instance = el[instanceName]

            if (options) {
                instance.setOptions && instance.setOptions(options)
            }

            call(instance, method)

            function call(instance, method) {
                method = typeof method !== 'string' ? defaultMethod : method
    
                if (method) {
                    if (!instance.hasOwnProperty(method)) {
                        throw new Error(`invalid method ${method}`)
                    }
                    instance[method].apply(instance, args)
                }
            }
        }
    }
}