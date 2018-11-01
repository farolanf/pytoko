once(function sortBar() {

    const el = document.querySelector('.sort-bar')
    init(el)

    $(document).on('pjax:end', e => {
        const el = e.target.querySelector('.sort-bar')
        init(el)
    })

    function init (el) {
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
