<template lang="pug">
    .navbar-item.has-dropdown.is-hoverable
        a.navbar-link(@click="show = !show") Kategori
        .navbar-dropdown(v-if="category.length")
            category-dropdown-item(v-for="item in category[0].children" :key="item.id" :item="item" hoverable @select="select")
</template>

<script>
export default {
    data () {
        return {
            show: false,
            showId: null,
        }
    },
    computed: mapState('cache', ['category']),
    methods: {
        select (item) {
            console.log(item)
        }
    }
}
</script>

<style lang="stylus">
.navbar-dropdown
    width 200px
    & .dropdown, & .dropdown-menu
        width 100%
</style>
