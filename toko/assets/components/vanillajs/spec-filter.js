once(function specFilter () {

    const el = document.querySelector('.specs-filter')

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
                        Warna: value
            */
            filters: {
                product: {},
                spec: {}
            }
        },
        computed: {
            hasFilters () {
                return Object.keys(this.filters.product).length ||
                    Object.keys(this.filters.spec).length
            }
        },
        methods: {
            toggleFilter (e) {
                const filter = $(e.target).data('filter')
                const label = $(e.target).data('filter-label')
                const value = $(e.target).data('filter-value')
                if (label) {
                    if (this.filters[filter][label]) {
                        this.$delete(this.filters[filter], label)
                    } else {
                        this.$set(this.filters[filter], label, value)
                    }
                } else {
                    this.$set(this.filters[filter], value, !this.filters[filter][value])
                }
                console.log(this.filters)
            },
            clearFilters () {

            }
        }
    })
})