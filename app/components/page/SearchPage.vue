<template lang="pug">
    j-page(title="Cari")
        .columns.is-multiline
            
            .column.is-12(v-for="(item, i) in data.results" :key="item.id * 10")
                router-link(:to="adDetail(item.id)")
                    ad-search-item-bar(:item="item" type="premium")

            .column.is-3(v-for="(item, i) in data.results" :key="item.id")
                router-link(:to="adDetail(item.id)")
                    ad-search-item(:item="item")

        pagination-nav.mt4(:max="8" :max-mobile="3" :data="data" :loading="loading")
</template>

<script>
export default {
    data () {
        return {
            data: {},
            loading: false,
        }
    },
    watch: {
        '$route' () {
            this.refresh()
        }
    },
    methods: {
        adDetail (id) {
            return { name: 'ad-detail', params: { id }}
        },
        type (i) {
            return i === 0 ? 'premium' 
                : i === 1 ? 'plus' : 'default'
        },
        refresh () {
            this.loading = true
            axios.get('/api/ads/', {
                params: this.$route.query
            }).then(resp => {
                this.data = resp.data
            }).finally(() => {
                this.loading = false
            })
        }
    },
    created () {
        this.refresh()
    }
}
</script>

