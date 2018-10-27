once(function searchBar () {

    $('.search-bar').each((i, el) => init(el))

    function init (el) {
        new Vue({
            el,
            template: el.outerHTML,
            delimiters: ['${', '}'],
            data() {
                return {
                    fresh: $(el).data('fresh'),
                    query: '',
                    suggestions: [],
                    visible: false
                }
            },
            watch: {
                suggestions (val) {
                    this.visible = val.length > 0
                }
            },
            methods: {
                show () {
                    this.visible = this.suggestions.length > 0
                },
                hide () {
                    this.visible = false
                },
                onQueryInput () {
                    this.fetchSuggestions()
                },
                onSuggestion (item, search = false) {
                    this.query = item.text
                    this.$refs.input.focus()
                    this.visible = false
                    search && this.search(item.text, item.category)
                },
                search (query, category) {
                    url = URLParse(document.URL)
                    q = { 
                        q: query,
                        page: 1
                    }
                    if (!category && this.fresh) {
                        category = ''
                    }
                    if (typeof category !== 'undefined') {
                        q.category = category
                    }
                    updateQuery = url.pathname === '/search/'
                    utils.setUrl('/search/', q, updateQuery)
                },
                fetchSuggestions () {
                    $.getJSON('/search/suggest/', { q: this.query }).then(data => {
                        this.suggestions = data.options
                        this.suggestions.length && this.suggestions.unshift({
                            'text': this.query,
                            'category': '',
                            'category_path': 'Semua kategori'
                        })
                    })
                }
            },
            created () {
                this.fetchSuggestions = _.debounce(this.fetchSuggestions, 200)
            },
            mounted () {
                this.$refs.input.focus()
            }
        })
    }
})