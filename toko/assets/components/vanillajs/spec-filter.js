once(function specFilter () {

    init(document)

    utils.pjaxReinit('.search-filter__side', init)

    function init (container) {
        const el = container.querySelector('.specs-filter')
        if (!el) return

        new Vue({
            el,
            template: el.outerHTML,
            data: {
                /*
                    filters
                        product
                            Handphone: true
                            Laptop: true
                        spec
                            Handphone
                                Warna: value
                */
                filters: {
                    product: parseProductQuery(),
                    spec: parseSpecQuery()
                }
            },
            computed: {
                hasFilters () {
                    return Object.keys(this.filters.product).find(title => {
                        return this.filters.product[title]
                    }) || Object.keys(this.filters.spec).find(product => {
                        return Object.keys(this.filters.spec[product]).find(label => {
                            return this.filters.spec[product][label] && 
                                this.filters.spec[product][label].length
                        })
                    })
                },
                productFilterQueryStr () {
                    // product[0]=product1&product[1]=product2,...
                    const arr = Object.keys(this.filters.product)
                        .map(title => this.filters.product[title] ? title : null)
                        .filter(item => item)
                    return JSON.stringify(arr)
                },
                specFilterQueryStr () {
                    return JSON.stringify(this.filters.spec)
                }
            },
            watch: {
                filters: {
                    handler () {
                        this.search()
                    },
                    deep: true
                }
            },
            methods: {
                specFilterActive (product, label, value) {
                    if (!isNaN(value)) {
                        value = +value
                    }
                    return this.filters.spec[product] && this.filters.spec[product][label] &&
                        this.filters.spec[product][label].includes(value)
                },
                toggleProductFilter (e) {
                    const title = $(e.target).data('filter-title')
                    this.$set(this.filters.product, title, !this.filters.product[title])
                },
                toggleSpecFilter (e) {
                    const product = $(e.target).data('filter-product')
                    const label = $(e.target).data('filter-label')
                    const value = $(e.target).data('filter-value')

                    if (!this.filters.spec[product]) {
                        this.$set(this.filters.spec, product, {})
                    }
                    
                    if (!this.filters.spec[product][label]) {
                        this.$set(this.filters.spec[product], label, [])
                    }

                    if (this.filters.spec[product][label].includes(value)) {
                        const i = this.filters.spec[product][label].indexOf(value)
                        this.filters.spec[product][label].splice(i, 1)
                        if (this.filters.spec[product][label].length <= 0) {
                            this.$delete(this.filters.spec[product], label)
                            if (Object.keys(this.filters.spec[product]).length <= 0) {
                                this.$delete(this.filters.spec, product)
                            }
                        }
                    } else {
                        this.filters.spec[product][label].push(value)
                    }
                },
                clearFilters () {
                    this.filters.product = {}
                    this.filters.spec = {}
                },
                search () {
                    const url = new URLParse(document.URL, true)
                    url.query.product = this.productFilterQueryStr
                    url.query.spec = this.specFilterQueryStr
                    url.query.page = 1
                    utils.pjax({
                        url: url.toString(),
                        container: '.search__results',
                        scrollTo: false,
                        fragment: '.search__results'
                    }, ['.search-filter', '.search-filter__side'])
                }
            }
        })
    }

    function parseProductQuery () {
        const product = {}
        const url = new URLParse(document.URL, true)
        if (url.query.product) {
            const arr = JSON.parse(url.query.product)
            arr.forEach(key => {
                product[key] = true
            })
            return product
        }
        return {}
    }

    function parseSpecQuery () {
        const url = new URLParse(document.URL, true)
        if (url.query.spec) {
            return JSON.parse(url.query.spec)
        }
        return {}
    }
})