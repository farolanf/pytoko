once(function sortBar() {
    
    $(".sort-bar").on("click", ".button", function(e) {
        $(e.delegateTarget).toggleClass("is-active");
    });

    $('.sort-bar .dropdown-menu .dropdown-item').on('click', function (e) {
        const sortType = $(e.target).text()
        utils.setUrl('/search/', { sort: sortType, page: 1 }, true)
    })
});
