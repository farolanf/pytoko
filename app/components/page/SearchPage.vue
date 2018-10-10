<template lang="pug">
    j-page(title="Cari")
        .columns.is-multiline
            
            .column.is-12(v-if="premium")
                router-link.link.dim.near-black(:to="adDetail(premium.id)")
                    ad-search-item-bar(:item="premium" type="premium")

            .column.is-3(v-for="(item, i) in data.results" :key="item.id")
                router-link(:to="adDetail(item.id)")
                    ad-search-item(:item="item")

        pagination-nav.mt4(:max="6" :max-mobile="3" :data="data" :loading="loading")
</template>

<script>
import { scrollTo } from '#/utils/dom'

export default {
    data () {
        return {
            data: {},
            premium: null,
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

            const query = { params: this.$route.query }

            return Promise.all([
                axios.get('/api/ads/premium/', query).then(resp => {
                    this.premium = resp.data
                }),
                axios.get('/api/ads/', query).then(resp => {
                    this.data = resp.data
                })
            ]).finally(() => {
                this.loading = false
            })
        }
    },
    created () {
        this.refresh()
    }
}
</script>

