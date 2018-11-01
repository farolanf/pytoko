once(function sortBar() {
    
    init()

    $(document).on('pjax:end', init)

    function init (e) {
        const container = e && e.target || document

        $(".sort-bar", container).on("click", ".button", function(e) {
            $(e.delegateTarget).toggleClass("is-active");
        });

        $('.sort-bar .dropdown-menu .dropdown-item', container).on('click', function (e) {
            const sortType = $(e.target).text()
            utils.setUrl('/search/', { sort: sortType, page: 1 }, true)
        })
    }
});
