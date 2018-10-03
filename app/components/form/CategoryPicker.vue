<template lang="pug">
    .category-picker.dropdown(:class="{'is-active': show}")
        
        .dropdown-trigger
            .breadcrumb.has-succeeds-separator.mb1
                ul 
                    li(v-if="!value") 
                        a(@click="show = !show") Pilih

                    li(v-for="(id, i) in selectedPath" v-if="i > 0" :key="id")
                        a.has-text-grey(v-if="!isLeaf(id)" @click="show = !show") {{ categoryIndex[id].name }} 
                        a(v-else @click="show = !show") {{ categoryIndex[id].name }}

        .dropdown-menu
            .dropdown-content
                .dropdown-item.has-text-centered(v-if="!category")
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
            category: null,
            showId: 0,
            show: false
        }
    },
    computed: {
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
        categoryIndex () {
            const index = {}
            this.category && this.traverseCategory(this.category[0], item => {
                index[item.id] = item
            })
            return index
        }
    },
    methods: {
        traverseCategory (item, cb) {
            cb(item)
            item.children && item.children.forEach(item => {
                this.traverseCategory(item, cb)
            })
        },
        select (id) {
            this.show = false
            this.$emit('input', id)
        },
        isLeaf (id) {
            return !this.categoryIndex[id].children || !this.categoryIndex[id].children.length
        }
    },
    mounted () {
        axios.get('/api/taxonomy/', {
            params: {
                slug: 'kategori'
            }
        }).then(resp => {
            this.category = resp.data
        })
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
