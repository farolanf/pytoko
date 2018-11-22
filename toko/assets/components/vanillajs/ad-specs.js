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
            const others = ['lainnya', 'lain-lain']
            data = data.filter(x => !others.includes(x.title.toLowerCase()))
                .concat(data.filter(x => others.includes(x.title.toLowerCase())))
            const $sel = $('[name="product_type"]')
            const val = $sel.val()
            $sel.html(
                data.map(x => `<option value="${x.id}">${x.title}</option>`).join('')
            )
            // restore value
            if ($(`option[value="${val}"]`, $sel).length) {
                $sel.val(val)
            } else {
                $sel.val($('option:first-child', $sel).val())
            }
            $sel.trigger('change')
        })
    }).trigger('change')

    function specValueMap () {
        return DATA.specs.reduce((obj, item) => {
            obj[item.field] = item.value
            return obj
        }, {})
    }
})