<template lang="pug">
    .ad-search-item.card.flex.flex-column(:class="{[theme.cardCls]: true}")
        .card-image
            figure.ad-search-item__figure.image.w-100.overflow-hidden
                img.h-100.of-cover(v-if="firstImage" :src="firstImage.image")
        .card-content.pa2.bt.b--light-gray.flex.flex-column.flex-grow-1
            p {{ item.title }}
            div.flex-grow-1.flex.justify-end.items-end
                div(:is="theme.tag").tag.is-rounded(:class="{[theme.tagCls]: true}") {{ money(item.price) }}
</template>

<script>
import info from '@/mixins/info'

export default {
    mixins: [info],
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
        },
        categoryPath () {
            return this.categoryPathStr(this.item.category)
        },
        provinsi () {
            return this.provinsiStr(this.item.provinsi)
        },
        kabupaten () {
            return this.kabupatenStr(this.item.provinsi, this.item.kabupaten)
        }
    }
}
</script>

<style lang="stylus">
.ad-search-item
    height 316px
.ad-search-item__small
    font-size .6rem
.ad-search-item__figure
    height 200px
    img
        height 100%
.ad-search-item--premium
    outline 4px solid #00d1b2
    box-shadow 2px 2px 15px 2px rgba(0, 0, 0, 0.3)
.ad-search-item--plus
    outline 2px solid #209cee
    box-shadow 2px 2px 5px 2px rgba(0, 0, 0, 0.3)
</style>