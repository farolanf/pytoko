<template lang="pug">
    .box
        .media.overflow-hidden
            .media-left
                figure.image.is-128x128
                    img(v-if="hasImage" :src="data.images[0].image")
            .media-content
                .content
                    .heading {{ categoryPath }}
                    p.f3 {{ data.title }}
                        span.heading {{ data.updated_at }}
                        span.heading {{ kabupaten }} - {{ provinsi }}
                    p {{ data.desc }}
                    .flex.flex.justify-end
                        .tag {{ money(data.price) }}
</template>

<script>
import info from '@/mixins/info'

export default {
    mixins: [info],
    props: {
        data: {
            type: Object,
            required: true
        }
    },
    computed: {
        hasImage () {
            return this.data.images && this.data.images.length
        },
        categoryPath () {
            return this.categoryPathStr(this.data.category)
        },
        provinsi () {
            return this.provinsiStr(this.data.provinsi)
        },
        kabupaten () {
            return this.kabupatenStr(this.data.provinsi, this.data.kabupaten)
        }
    },
}
</script>

