<template lang="pug">
    .navbar-item.has-dropdown(:class="{'is-hoverable': show}")
        a.navbar-link(@click="show = show ? hide() : true") Kategori
        .navbar-dropdown(v-if="category.length")
            category-dropdown-item(v-for="item in category[0].children" :key="item.id" :item="item" :show-ids="showIds" @select="select")
</template>

<script>
export default {
    data () {
        return {
            show: true,
            showIds: [],
        }
    },
    computed: mapState('cache', ['category', 'categoryPaths']),
    methods: {
        ...mapActions('cache', ['getCategory']),
        select (e) {
            // TODO: fix dropdown expand state
            if (e.item.isLeaf) {
                this.showIds = []
            } else {
                this.showIds = this.showIds.slice(0, e.depth + 1)
                this.$set(this.showIds, e.depth, 
                    this.showIds[e.depth] === e.item.id ? false : e.item.id)
            }
            this.hide()
            this.$router.push({
                name: 'search',
                query: { category: e.item.id }
            })
        },
        hide () {
            this.show = false
            setTimeout(() => { this.show = true }, 100)
        }
    },
    created () {
        this.getCategory()
    }
}
</script>

<style lang="scss">
@import '~bulma/sass/utilities/all';

@include until($tablet) {
    .navbar-dropdown {
        width: 100%;
    }
}

@include from($tablet) {
    .navbar-dropdown {
        width: 200px;
    }
}
</style>
