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
        ...mapState('cache', ['categoryPaths', 'provinsiMap', 'kabupatenMap']),
        hasImage () {
            return this.data.images && this.data.images.length
        },
        categoryPath () {
            return this.categoryPaths[this.data.category] 
                ? this.categoryPaths[this.data.category]
                    .slice(1)
                    .map(item => item.name)
                    .join(' / ')
                : ''
        },
        provinsi () {
            return this.provinsiMap[this.data.provinsi] ? this.provinsiMap[this.data.provinsi].name : ''
        },
        kabupaten () {
            if (!this.kabupatenMap[this.data.kabupaten]) {
                this.getKabupaten({ provinsiId: this.data.provinsi })
                return
            }
            return this.kabupatenMap[this.data.kabupaten] ? this.kabupatenMap[this.data.kabupaten].name : ''
        }
    },
    methods: mapActions('cache', ['getCategory', 'getProvinsi', 'getKabupaten']),
    mounted () {
        this.getCategory()
        this.getProvinsi()
    }
}
</script>

