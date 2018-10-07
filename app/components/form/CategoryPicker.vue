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
                    category-dropdown-item(v-for="item in category[0].children" :key="item.id" :item="item" :show-ids="showIds" @select="select")
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
            show: false,
            showIds: [],
        }
    },
    computed: {
        ...mapState('cache', ['category', 'categoryMap', 'categoryPaths']),
        ...mapGetters('cache', ['getCategoryPathIds']),
        selectedPath () {
            if (!this.value) return
            return this.categoryPaths[this.value]
        },
    },
    methods: {
        ...mapActions('cache', ['getCategory']),
        select (e) {
            if (this.isLeaf(e.item)) {
                this.show = false
                this.showIds = this.getCategoryPathIds(e.item.id)
                this.$emit('input', e.item.id)
            } else {
                this.showIds = this.showIds.slice(0, e.depth + 1)
                this.$set(this.showIds, e.depth, 
                    this.showIds[e.depth] === e.item.id ? false : e.item.id)
            }
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
