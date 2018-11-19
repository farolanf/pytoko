once(function adSpecs () {

    const el = $('.specs-container').get(0)

    const vm = new Vue({
        el: el,
        template: el.outerHTML,
        delimiters: DATA.delimiters,
        data: {
            productType: '',
            specs: [],
            values: DATA.specs.map(x => x.value),
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
})