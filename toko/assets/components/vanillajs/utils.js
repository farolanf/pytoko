const utils = {

    /**
     * Pjax with multiple containers support.
     * 
     * @param {object} opts Pjax options
     * @param {array} conSelectors Additional container-selectors
     */
    pjax (opts, conSelectors) {

        // emit pjax:reinit with a list of container-elements
        $(document).one('pjax:end', function (e, response) {
            const $data = $(response.responseText)
            conSelectors.unshift(opts.fragment || '')
            let containers = []
            conSelectors.map(selector => {
                const newCon = getElement(selector, $data)
                if (newCon) {
                    const cons = $(document).find(selector).toArray()
                    containers = containers.concat(cons)
                }
            })
            $(document).trigger('pjax:reinit', [containers])
        })

        // replace additional containers
        if (conSelectors && conSelectors.length) {
            $(document).one('pjax:success', function (e, data) {
                const $data = $(data)
                const pjaxCon = this
                conSelectors.forEach(conSelector => {
                    const newCon = getElement(conSelector, $data)
                    if (newCon) {
                        $(conSelector, pjaxCon).replaceWith(newCon.outerHTML)
                    }
                })
            })
        }

        $.pjax(opts)

        function getElement (selector, $data) {
            if (!selector) return $data.get(0)
            let $el = $data.filter(selector)
            if (!$el.length) {
                $el = $data.find(selector)
            }
            return $el.get(0)
        }
    },

    /**
     * Call the function with container matching or containing the selector.
     * 
     * @param {string} selector 
     * @param {function} fn 
     */
    pjaxReinit (selector, fn) {
        $(document).on('pjax:reinit', (e, containers) => {
            containers.forEach(con => {
                if ($(con).is(selector) || $(con).find(selector).length) {
                    fn(con)
                }
            })
        })
    },

    setUrl (pathname, query, update = false) {
        const url = URLParse(document.URL, true)
        pathname && url.set('pathname', pathname)
        url.set('query', update ? Object.assign({}, url.query, query) : query)
        window.location.assign(url.toString())
    },

    parseQueryArray (str) {
        const parts = str.split('&')
        const arr = []
        parts.forEach(part => {
            const m = part.match(/(?:.+)\[(\d+)\]=(.+)/)
            if (m) {
                arr[m[1]] = m[2]
            }
        })
        return arr
    },

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
    },

    lastSegment (url) {
        return url.slice(url.lastIndexOf('/') + 1)
    }
}