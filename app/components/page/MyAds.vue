<template lang="pug">
    j-page.my-ads-page(title="Iklan Saya")

        template(v-if="data")

            router-link.black-80(v-for="ad in data.data" :key="ad.id" :to="editAdUrl(ad.id)")
                .flex-column.pa4.w-100.shadow-4.mb4.dim.pointer
                    .f3 {{ ad.title }}
                    .f7.mt2 Diperbarui {{ ad.updated_at }}
                    p.ml4.mt3 {{ ad.desc }}

            pagination-nav(:max="8" :max-mobile="3" :data="data" :loading="loading" @change="toPage")
</template>

<script>
export default {
    data () {
        return {
            data: null,
            loading: false
        }
    },
    watch: {
        '$route' () {
            this.fetch()
        }
    },
    methods: {
        toPage (num) {
            this.$router.push({ query: { page: num } })
        },
        editAdUrl (id) {
            return this.$router.resolve({
                name: 'edit-ad', 
                params: { id }
            }).href
        },
        fetch () {
            this.loading = true
            axios.get('/api/ads', { params: { page: this.$route.query.page } })
                .then(resp => {
                    this.data = resp.data
                })
                .finally(() => {
                    this.loading = false
                })
        }
    },
    mounted () {
        this.fetch()
    }
}
</script>


<style lang="scss">
@import '~bulma/bulma';

.my-ads-page {
    @include from($tablet) {
        .nav.pagination {
            float: right;
        }
    }
}
</style>
