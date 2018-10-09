<template lang="pug">
    j-page.my-ads-page(title="Iklan Saya")

        template(v-if="data")

            router-link.black-80(v-for="ad in data.results" :key="ad.id" :to="editAdUrl(ad.id)")
                ad-list-item.mb4(:data="ad")

            pagination-nav.mt1(:max="8" :max-mobile="3" :data="data" :loading="loading")
</template>

<script>
export default {
    data () {
        return {
            data: null,
        }
    },
    watch: {
        '$route' () {
            this.fetch()
        }
    },
    methods: {
        editAdUrl (id) {
            return this.$router.resolve({
                name: 'edit-ad', 
                params: { id }
            }).href
        },
        fetch () {
            this.loading = true
            axios.get('/api/ads/', { params: { page: this.$route.query.page } })
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
@import '~bulma/sass/utilities/all';

.my-ads-page {
    @include from($tablet) {
        .nav.pagination {
            float: right;
        }
    }
}
</style>
