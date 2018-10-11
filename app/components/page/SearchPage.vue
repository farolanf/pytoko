<template lang="pug">
    j-page(title="Cari")
        search-box
        .tile.is-ancestor.is-vertical
            
            .tile.is-12.is-parent(v-if="premium")
                .tile.is-child
                    router-link.link.dim.near-black(:to="adDetail(premium.id)")
                        ad-search-item-bar(:item="premium" type="premium")

            .tile.is-12.is-parent(v-for="(row, i) in rows" :key="i")
                .tile.is-3.is-child.pa2(v-for="item in row" :key="item.id")
                    router-link(:to="adDetail(item.id)")
                        ad-search-item.h-100(:item="item")

        pagination-nav.mt4(:max="6" :max-mobile="3" :data="data" :loading="loading")
</template>

<script>
import { prepareAd } from '#/utils/data'
import { scrollTo } from '#/utils/dom'

export default {
    data () {
        return {
            data: {},
            premium: null,
            loading: false,
        }
    },
    computed: {
        rows () {
            let count = 0
            const map = _.groupBy(this.data.results, item => {
                return Math.floor(count++ / 4) 
            })
            return Object.values(map)
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
                    this.premium = prepareAd(resp.data)
                }),
                axios.get('/api/ads/', query).then(resp => {
                    this.data = resp.data
                    this.data.results = this.data.results.map(prepareAd)
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

<style lang="scss">
@import '~bulma/sass/utilities/all';

@include until($tablet) {
    .search-page__tile {
        flex: none;
        width: 100%;
    }
}
@include from($tablet) {
    .search-page__tile {
        flex: none;
        width: 20%;
    }
}
</style>
