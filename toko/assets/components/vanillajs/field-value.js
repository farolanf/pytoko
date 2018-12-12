(function ($) {
    
    $(init)

    function init () {
        const $rows = $('[id^="specs-"].has_original')
        if ($rows.length) {
            $rows.each((i, el) => {
                initSelect(el.querySelector('.field-field select'), el.querySelector('.field-value select'))
            })
        } else {
            initSelect(document.querySelector('.field-field select'), document.querySelector('.field-value select'))
        }
    }

    function initSelect (fieldSelect, valueSelect) {
        $(fieldSelect).on('change', function () {
            const fieldId = this.value
            if (!fieldId) {
                valueSelect.innerHTML = ''
                return
            }
            $.ajax({
                url: '/values/field/',
                data: { 'id': fieldId }
            }).then(data => {
                const html = data
                    .map(x => `<option value="${x.id}">${x.value}</option>`)
                    .join('')
                $(valueSelect).html(html)
            })
        })
    }

})(django.jQuery)
