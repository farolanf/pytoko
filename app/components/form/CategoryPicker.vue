<template lang="pug">
    .category-picker.dropdown(:class="{'is-active': show}")
        
        .dropdown-trigger
            .breadcrumb.has-succeeds-separator.mb1
                ul 
                    li(v-if="!value") 
                        a(@click="show = !show") Pilih

                    li(v-for="(item, i) in selectedPath" v-if="i > 0" :key="item.id")
                        a.has-text-grey(v-if="!isLeaf(item)" @click="show = !show") {{ item.name }} 
                        a(v-else @click="show = !show") {{ item.name }}

        .dropdown-menu
            .dropdown-content
                .dropdown-item.has-text-centered(v-if="!category.length")
                    button.button.is-text.is-loading
                template(v-else)
                    category-dropdown-item(v-for="item in category[0].children" :key="item.id" :item="item" :show-id.sync="showId" :selected-id="value" :on-select="select")
</template>

<script>
export default {
    props: {
        value: {
            required: true
        }
    },
    data () {
        return {
            showId: 0,
            show: false
        }
    },
    computed: {
        ...mapState('cache', ['category', 'categoryMap', 'categoryPaths']),
        selectedPath () {
            if (!this.value) return
            return this.categoryPaths[this.value]
        },
    },
    methods: {
        ...mapActions('cache', ['getCategory']),
        select (id) {
            this.show = false
            this.$emit('input', id)
        },
        isLeaf (item) {
            return !item.children || !item.children.length
        }
    },
    mounted () {
        this.getCategory()
    }
}
</script>

<style lang="scss">
@import '~bulma/bulma';

@include until($tablet) {
    .category-picker.dropdown {
        width: 100%;
        & > .dropdown-menu {
            width: 100%;
        }
    }
}
</style>
