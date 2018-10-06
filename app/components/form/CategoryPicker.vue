<template lang="pug">
    .category-picker.dropdown(:class="{'is-active': show}")
        
        .dropdown-trigger
            .breadcrumb.has-succeeds-separator.mb1
                ul 
                    li(v-if="!value") 
                        a(@click="show = !show") Pilih

                    li(v-for="(id, i) in selectedPath" v-if="i > 0" :key="id")
                        a.has-text-grey(v-if="!isLeaf(id)" @click="show = !show") {{ categoryMap[id].name }} 
                        a(v-else @click="show = !show") {{ categoryMap[id].name }}

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
        ...mapState('cache', ['category', 'categoryMap']),
        selectedPath () {
            if (!this.value) return
            const id = this.value
            const stack = []
            let state = {
                item: this.category[0],
                i: 0,
            }
            do {
                if (state.item.children && state.item.children.length 
                        && state.i < state.item.children.length) {
                    stack.push(state)
                    state = {
                        item: state.item.children[state.i++],
                        i: 0,
                    }
                    if (state.item.id === id) {
                        stack.push(state)
                        break;
                    }
                } else {
                    state = stack.pop()
                }
            } while (state)
            return stack.map(state => state.item.id)
        },
    },
    methods: {
        ...mapActions('cache', ['getCategory']),
        select (id) {
            this.show = false
            this.$emit('input', id)
        },
        isLeaf (id) {
            return !this.categoryMap[id].children || !this.categoryMap[id].children.length
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
