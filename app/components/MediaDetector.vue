<template lang="pug">
    div
        div.dn.is-block-mobile(ref="mobile")
        div.dn.is-block-tablet(ref="tablet")
</template>

<script>
export default {
    methods: {
        ...mapMutations(['setMedia']),
        detect () {
            const mobile = getComputedStyle(this.$refs.mobile).display === 'block'
            const tablet = getComputedStyle(this.$refs.tablet).display === 'block'
            this.setMedia({ mobile, tablet })
            this.timeout = setTimeout(this.detect, 1000)
        }
    },
    mounted () {
        this.detect()
    },
    beforeDestroy () {
        clearTimeout(this.timeout)
    }
}
</script>

