<template lang="pug">
    div.category-dropdown-item.relative
        a.dropdown-item(:class="{'is-active': active, 'has-background-light': show && !active}" @click="$emit('select', { item, depth })")
            template {{ item.name }}
            span.icon(v-if="hasChildren")
                i.fa.fa-angle-right

        .dropdown(v-if="hasChildren" :class="{'is-active': show}")
            
            .dropdown-menu
                .dropdown-content
                    category-dropdown-item(v-for="child in item.children" :key="child.id" :item="child" :depth="depth + 1" :show-ids="showIds" @select="$emit('select', $event)")
</template>

<script>
export default {
    props: {
        item: {
            type: Object
        },
        showIds: {
            type: Array,
            default () {
                return []
            }
        },
        depth: {
            type: Number,
            default: 0
        }
    },
    computed: {
        show () {
            return this.showIds.includes(this.item.id)
        },
        active () {
            return this.show && !this.hasChildren
        },
        hasChildren () {
            return this.item.children && this.item.children.length
        }
    },
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
    & > .dropdown:not(.is-active) > .dropdown-menu
        display none
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
        .dropdown.is-active > .dropdown-menu {
            display: block;
        }
    }
}

@include from($tablet) {
    .category-dropdown-item {
        & > .dropdown {
            top: 0;
            left: 100%;
        }
        &:hover > .dropdown > .dropdown-menu {
            display: block;
        }
        & .dropdown, & .dropdown-menu {
            width: 100%;
        }
    }
}
</style>
