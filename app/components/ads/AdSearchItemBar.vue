<template lang="pug">
    .card.is-hidden-tablet(v-if="mobile" :class="{[theme.cls]: true}")
        .card-image.image
            img.of-cover(v-if="item.images[0]" :src="item.images[0].image")
        .card-content
            p.heading {{ item.updated_at }}
            p.heading {{ categoryPath }}
            strong.f4 {{ item.title }}
            p.heading {{ kabupaten }} - {{ provinsi }}
            p.ad-search-item-bar__desc {{ item.desc }}
            div(:is="theme.tag").tag.is-rounded(:class="{[theme.tagCls]: true}") Rp30.000

    .is-hidden-mobile(v-else-if="tablet")
        article.ad-search-item-bar.media.pa2.pr4.overflow-hidden(:class="{[theme.cls]: true}")
            .media-left.w-30
                .tile.is-ancestor
                    .tile.is-parent
                        .tile.is-image.is-child
                            img.of-cover(v-if="item.images[0]" :src="item.images[0].image")
                        .tile.is-image.is-child
                            img.of-cover(v-if="item.images[1]" :src="item.images[1].image")
                .flex
                    p.image
                        img.of-cover(v-if="item.images[2]" :src="item.images[2].image")
                    p.image
                        img.of-cover(v-if="item.images[3]" :src="item.images[3].image")
            .media-content.h-100
                p.heading {{ item.updated_at }}
                p.heading {{ categoryPath }}
                strong.f3 {{ item.title }}
                p.heading {{ kabupaten }} - {{ provinsi }}
                p.ad-search-item-bar__desc {{ item.desc }}
                .level.pt2
                    .level-left
                    .level-right
                        .level-item 
                            div(:is="theme.tag").tag.is-rounded(:class="{[theme.tagCls]: true}") Rp30.000
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
.ad-search-item-bar
    height 320px
.ad-search-item-bar__desc
    position relative
    height 166px
    overflow hidden
.ad-search-item-bar__desc::after
    content ' '
    position absolute
    bottom 0
    left 0
    width 100%
    height 4rem
    background linear-gradient(transparent, white)
.ad-search-item-bar--premium
    outline 5px solid #00d1b2
    box-shadow 2px 2px 15px 2px rgba(0, 0, 0, 0.3)
.ad-search-item-bar--plus
    outline 2px solid #209cee
    box-shadow 2px 2px 5px 2px rgba(0, 0, 0, 0.3)
</style>