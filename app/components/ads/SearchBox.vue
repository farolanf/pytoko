<template lang="pug">
    .box
        form(@submit.prevent="submit")
            .field.is-horizontal
                .field-label.is-normal
                    label.label Kategori
                .field-body
                    .field
                        .control
                            .select
                                select(v-model="category")
                                    option(v-for="id in info.categories" :key="id" :value="id") {{ categoryPathStr(id) }}
                    .field
                        .control
                            input.input

        div Hasil: {{ info.count }}
</template>

<script>
import info from '@/mixins/info'

export default {
    mixins: [info],
    data () {
        return {
            category: null,
            info: {},
        }
    },
    computed: {
        query () {
            return this.$route.query
        }
    },
    watch: {
        category (val) {
            this.$router.push({ 
                query: Object.assign({}, this.query, {
                    category: val
                })
            })
        },
        '$route' () {
            this.getInfo()
        }
    },
    methods: {
        submit () {

        },
        getInfo () {
            axios.get('/api/ads/info/', { params: this.query })
                .then(resp => {
                    this.info = resp.data
                })
        },
    },
    mounted () {
        this.getInfo()
    }
}
</script>

