once(function sortBar() {

    init(document)

    utils.pjaxReinit('.search__main', init)

    function init (container) {
        const el = container.querySelector('.sort-bar')
        if (!el) return

        new Vue({
            el,
            template: el.outerHTML,
            data: {
                visible: false,
            },
            methods: {
                show () {
                    this.visible = true
                },
                hide () {
                    this.visible = false
                },
                onSort (e) {
                    const sortType = e.target.innerText
                    utils.setUrl('/search/', { sort: sortType, page: 1 }, true)
                    this.hide()
                }
            }
        })
    }
});
