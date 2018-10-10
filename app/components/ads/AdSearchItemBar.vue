<template lang="pug">
    article.media(:class="{[theme.cls]: true}")
        figure.media-left.overflow-hidden
            p.image.is-square.w-50
                img.of-cover(v-if="item.images[0]" :src="item.images[0].image")
        .media-content
            p.f3 {{ item.title }}
            .level
                .level-left
                .level-right
                    .level-item 
                        div(:is="theme.tag").tag.is-rounded(:class="{[theme.tagCls]: true}") Rp30.000
</template>

<script>

export default {
    props: {
        item: {
            type: Object,
            required: true
        },
        type: {
            type: String,
            default: 'default'
        }
    },
    data () {
        return {
            types: {
                premium: {
                    cls: 'ad-search-item-bar--premium',
                    tag: 'strong',
                    tagCls: 'is-primary',
                },
                plus: {
                    cls: 'ad-search-item-bar--plus',
                    tag: 'strong',
                    tagCls: 'is-info',
                },
                default: {
                    cls: '',
                    tag: 'span',
                    tagCls: 'is-light',
                }
            }
        }
    },
    computed: {
        firstImage () {
            return this.item.images && this.item.images[0]
        },
        theme () {
            return this.types[this.type]
        }
    }
}
</script>

<style lang="stylus">
.ad-search-item-bar--premium
    outline 4px solid #00d1b2
    box-shadow 2px 2px 15px 2px rgba(0, 0, 0, 0.3)

.ad-search-item-bar--plus
    outline 2px solid #209cee
    box-shadow 2px 2px 5px 2px rgba(0, 0, 0, 0.3)
</style>