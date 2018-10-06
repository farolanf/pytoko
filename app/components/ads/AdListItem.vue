<template lang="pug">
    .box
        .media.overflow-hidden
            .media-left
                figure.image.is-128x128
                    img(v-if="hasImage" :src="data.images[0].image")
            .media-content
                .content
                    p
                        strong.title {{ data.title }}
                        div.heading {{ data.updated_at }}
                    p {{ data.desc }}
</template>

<script>
export default {
    props: {
        data: {
            type: Object,
            required: true
        }
    },
    computed: {
        hasImage () {
            return this.data.images && this.data.images.length
        }
    }
}
</script>

