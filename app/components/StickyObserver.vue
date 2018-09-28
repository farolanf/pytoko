<template lang="pug">
    .sticky-observer__target    
</template>

<script>
export default {
    props: {
        target: {
            required: true
        },
        stickyClass: {
            type: String
        }
    },
    computed: {
        targetEl () {
            return typeof this.target === 'string' ? document.querySelector(this.target) : this.target
        }
    },
    mounted () {
        // counter toggle
        $(this.targetEl).toggleClass(this.stickyClass)

        const observer = new IntersectionObserver(() => {
            $(this.targetEl).toggleClass(this.stickyClass)
        })

        observer.observe(this.$el)
    }
}
</script>

<style lang="stylus">
.sticky-observer__target
    position absolute 
    top 0
    width 100%
    height 8px
</style>
