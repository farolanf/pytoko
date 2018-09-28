<template lang="pug">
    div.category-dropdown-item.relative
        a.dropdown-item(:class="{'is-active': active, 'has-background-light': show}" @click="click")
            template {{ item.title }}
            span.icon(v-if="hasChildren")
                i.fa.fa-angle-right

        .dropdown(v-if="show && hasChildren" :class="{'is-active': show}")
            
            .dropdown-menu
                .dropdown-content
                    category-dropdown-item(v-for="child in item.children" :key="child.id" :item="child" :show-id.sync="childShowId" :selected-id="selectedId" :on-select="onSelect")
</template>

<script>
export default {
    props: {
        item: {
            type: Object
        },
        showId: {
            type: Number
        },
        selectedId: {
            type: Number
        },
        onSelect: {
            type: Function
        }
    },
    data () {
        return {
            childShowId: 0
        }
    },
    computed: {
        show () {
            return this.showId === this.item.id
        },
        active () {
            return this.item.id === this.selectedId
        },
        hasChildren () {
            return this.item.children && Object.keys(this.item.children).length
        }
    },
    methods: {
        click () {
            if (this.hasChildren) {
                this.$emit('update:showId', this.showId === this.item.id ? 0 : this.item.id)
            } else {
                this.onSelect(this.item.id)
            }
        }
    }
}
</script>

<style lang="stylus">
.category-dropdown-item
    & > .dropdown-item
        padding-right 0.5rem
        display flex
        justify-content space-between
        align-items center
    & > .dropdown
        position absolute
</style>

<style lang="scss">
@import '~bulma/bulma';

@include until($tablet) {
    .category-dropdown-item {
        & > .dropdown {
            bottom: 0;
            left: 0;
            width: 100%;
            & > .dropdown-menu {
                width: 100%;
            }
        }
    }
}

@include from($tablet) {
    .category-dropdown-item {
        & > .dropdown {
            top: 0;
            left: 100%;
        }
    }
}
</style>
