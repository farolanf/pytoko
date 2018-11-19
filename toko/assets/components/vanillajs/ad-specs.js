once(function adSpecs () {

    const el = $('.specs-container').get(0)

    const vm = new Vue({
        el: el,
        template: el.outerHTML,
        delimiters: DATA.delimiters,
        data: {
            productType: '',
            specs: [],
            values: specValueMap(),
        },
        watch: {
            productType () {
                this.fetchSpecs()
            }
        },
        methods: {
            fetchSpecs () {
                $.ajax({
                    url: `/producttype/${this.productType}/specs/`,
                }).then(data => {
                    this.specs = data
                    this.values = specValueMap()
                })
            },
        },
        mounted () {
            $(this.$el).removeClass('dn')
        }
    })

    $('[name="product_type"]').on('change', function () {
        vm.productType = this.value
    }).trigger('change')

    $('[name="category"]').on('change', function () {
        $.ajax({
            url: '/producttype/',
            data: {
                categories: this.value
            }
        }).then(data => {
            $('[name="product_type"]').html(
                data.map(x => `<option value="${x.id}">${x.title}</option>`).join('')
            ).trigger('change')
        })
    }).trigger('change')

    function specValueMap () {
        return DATA.specs.reduce((obj, item) => {
            obj[item.field] = item.value
            return obj
        }, {})
    }
})