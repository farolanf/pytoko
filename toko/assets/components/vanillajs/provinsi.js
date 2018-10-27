(function () {

    $('select[name="provinsi"]').on('change', function () {
        $.getJSON('/kabupaten/', { provinsi_id: this.value })
            .then(renderOptions)
    })

    function renderOptions(data) {
        $('select[name="kabupaten"]').html('')
        data.forEach(item => {
            $('select[name="kabupaten"]')
                .append(`<option value="${item.id}">${item.name}</option>`)
        })
    }
})()
