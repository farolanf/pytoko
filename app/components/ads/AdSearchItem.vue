<template lang="pug">
    .card(:class="{[theme.cardCls]: true}")
        .card-image
            figure.image.is-square.w-100.overflow-hidden
                img.ad-search-item__img(v-if="firstImage" :src="firstImage.image")
        .card-content.pa2.bt.b--light-gray
            p.f6 {{ item.title }}
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
                    cardCls: 'ad-search-item--premium',
                    tag: 'strong',
                    tagCls: 'is-primary',
                },
                plus: {
                    cardCls: 'ad-search-item--plus',
                    tag: 'strong',
                    tagCls: 'is-info',
                },
                default: {
                    cardCls: '',
                    tag: 'strong',
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
.ad-search-item__img
    object-fit cover

.ad-search-item--premium
    outline 4px solid #00d1b2
    box-shadow 2px 2px 15px 2px rgba(0, 0, 0, 0.3)

.ad-search-item--plus
    outline 2px solid #209cee
    box-shadow 2px 2px 5px 2px rgba(0, 0, 0, 0.3)
</style>