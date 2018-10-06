<template lang="pug">
    .nav.pagination
        .container
            .columns
                .column

                    ul.list.flex.justify-center.is-hidden-tablet

                        li(v-if="firstVisible(maxMobile)")
                            a.pagination-link(:href="pageUrl(1)" @click.prevent="toPage(1)") 1
                            span.mh2.v-btm ...

                        li(v-for="page in prevPageUrls(maxMobile)" :key="page.url")
                            a.pagination-link(:href="page.url" @click.prevent="toPage(page.num)") {{ page.num }}
                        
                        li
                            a.pagination-link.is-current {{ data.page_num }}
                        
                        li(v-for="page in nextPageUrls(maxMobile)" :key="page.url")
                            a.pagination-link(:href="page.url" @click.prevent="toPage(page.num)") {{ page.num }}

                        li(v-if="lastVisible(maxMobile)")
                            span.mh2.v-btm ...
                            a.pagination-link(:href="pageUrl(lastPageNum)" @click.prevent="toPage(lastPageNum)") {{ lastPageNum }}

                    ul.list.flex.justify-end.is-hidden-mobile

                        li(v-if="firstVisible(max)")
                            a.pagination-link(:href="pageUrl(1)" @click.prevent="toPage(1)") 1
                            span.mh2.v-btm ...

                        li(v-for="page in prevPageUrls(max)" :key="page.url")
                            a.pagination-link(:href="page.url" @click.prevent="toPage(page.num)") {{ page.num }}
                        
                        li
                            a.pagination-link.is-current {{ data.page_num }}
                        
                        li(v-for="page in nextPageUrls(max)" :key="page.url")
                            a.pagination-link(:href="page.url" @click.prevent="toPage(page.num)") {{ page.num }}

                        li(v-if="lastVisible(max)")
                            span.mh2.v-btm ...
                            a.pagination-link(:href="pageUrl(lastPageNum)" @click.prevent="toPage(lastPageNum)") {{ lastPageNum }}

                .column.is-narrow
                    
                    a.pagination-previous(:href="pageUrl(data.page_num - 1)" title="Halaman sebelumnya" :disabled="prevDisabled" @click.prevent="prev") Sebelum
                    
                    a.pagination-next(:href="pageUrl(data.page_num + 1)" title="Halaman sesudahnya" :disabled="nextDisabled" @click.prevent="next") Sesudah
</template>

<script>
export default {
    props: {
        data: {
            type: Object,
            required: true
        },
        loading: {
            type: Boolean
        },
        max: {
            type: Number,
            default: 8
        },
        maxMobile: {
            type: Number,
            default: 3
        }
    },
    computed: {
        lastPageNum () {
            return Math.ceil(this.data.count / this.data.page_size)
        },
        prevDisabled () {
            return this.loading || this.data.page_num === 1
        },
        nextDisabled () {
            return this.loading || this.data.page_num >= this.lastPageNum
        }
    },
    methods: {
        firstVisible (max) {
            const end = Math.min(this.data.page_num + max, this.lastPageNum)
            const nextCount = end - this.data.page_num
            return (this.data.page_num - max - (max - nextCount)) > 1
        },
        lastVisible (max) {
            const start = Math.max(this.data.page_num - max, 1)
            const prevCount = this.data.page_num - start
            return (this.data.page_num + max + (max - prevCount)) < this.lastPageNum
        },
        prevPageUrls (max) {
            if (this.data.page_num <= 1) return
            
            // take invisble next count
            const end = Math.min(this.data.page_num + max, this.lastPageNum)
            const nextCount = end - this.data.page_num

            const start = Math.max(this.data.page_num - max - (max - nextCount), 1)
            
            // offset if first page visible
            const offset = start > 1 ? 2 : 0 

            // subtract 2 for first page nav and dots
            const count = this.data.page_num - start - offset

            return Array(count).fill(0).map((n, i) => {
                const num = start + i + offset
                return {
                    num,
                    url: this.pageUrl(num)
                }
            })
        },
        nextPageUrls (max) {
            if (this.data.page_num >= this.lastPageNum) return
            
            // take invisible prev count
            const start = Math.max(this.data.page_num - max, 1)
            const prevCount = this.data.page_num - start

            const end = Math.min(this.data.page_num + max + (max - prevCount), this.lastPageNum)
            // subtract 2 for last page nav and dots
            const count = end - this.data.page_num - (end < this.lastPageNum ? 2 : 0)

            return Array(count).fill(0).map((n, i) => {
                const num = this.data.page_num + i + 1 
                return {
                    num,
                    url: this.pageUrl(num)
                }
            })
        },
        prev () {
            if (this.prevDisabled) return
            this.toPage(this.data.page_num - 1)
        },
        next () {
            if (this.nextDisabled) return
            this.toPage(this.data.page_num + 1)
        },
        pageUrl (num) {
            if (num < 1 || num > this.lastPageNum) return
            return this.$router.resolve({ query: { page: num } }).href
        },
        toPage (num) {
            this.$emit('change', num)
        }
    }
}
</script>

