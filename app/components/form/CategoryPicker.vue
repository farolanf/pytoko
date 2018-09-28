<template lang="pug">
    .category-picker.dropdown(:class="{'is-active': show}")
        
        .dropdown-trigger
            .breadcrumb.has-succeeds-separator.mb1
                ul 
                    li(v-if="!value") 
                        a(@click="show = !show") Pilih

                    li(v-for="(id, key) in selectedPath" v-if="id && key !== 'id1'")
                        a.has-text-grey(v-if="!isLeaf(id)" @click="show = !show") {{ category.data[id].title }} 
                        a(v-else @click="show = !show") {{ category.data[id].title }}

        .dropdown-menu
            .dropdown-content
                .dropdown-item.has-text-centered(v-if="!category")
                    button.button.is-text.is-loading
                template(v-else)
                    category-dropdown-item(v-for="item in category.tree[0].children" :key="item.id" :item="item" :show-id.sync="showId" :selected-id="value" :on-select="select")
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
            return this.category && this.category.paths.find(path => {
                return Object.values(path).includes(this.value)
            })
        }
    },
    methods: {
        select (id) {
            this.show = false
            this.$emit('input', id)
        },
        isLeaf (id) {
            return this.category.leaves.includes(id)
        }
    },
    mounted () {
        axios.get('/api/categories')
            .then(resp => {
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
