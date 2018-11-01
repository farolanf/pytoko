once(function searchFilter () {

    init(document)

    utils.pjaxReinit('.search-filter', init)

    function init (container) {

        $('#category-filter', container).on('change', function () {
            if (this.value) {
                utils.setUrl('/search/', { category: this.value, page: 1 }, true)
            }
        })

        Vue.component('price-dropdown', {
            props: ['placeholder', 'value'],
            template: container.querySelector('#price-dropdown-template').innerHTML,
            delimiters: ['${', '}'],
            data () {
                return {
                    visible: false,
                }
            },
            methods: {
                inputChange (e) {
                    this.$emit('input', $(e.target).val())
                },
                optionClick (e) {
                    this.$emit('input', $(e.target).data('value'))
                    this.hide()
                },
                show () {
                    this.visible = true
                },
                hide () {
                    this.visible = false
                }
            }
        })

        const priceFilterEl = container.querySelector('.price-filter')

        const url = new URLParse(document.URL, true)

        const prices = (url.query.price || '').split('-')

        new Vue({
            el: priceFilterEl,
            template: priceFilterEl.outerHTML,
            data: {
                priceFrom: prices[0] || 0,
                priceTo: prices[1] || 0
            },
            watch: {
                priceFrom () {
                    this.search()
                },
                priceTo () {
                    this.search()
                }
            },
            methods: {
                search () {
                    const priceFrom = Math.min(this.priceFrom, this.priceTo)
                    const priceTo = Math.max(this.priceFrom, this.priceTo)
                    utils.setUrl('/search/', {
                        price: priceFrom || priceTo ? `${priceFrom}-${priceTo}` : ''
                    }, true)
                }
            }
        })
    }
})