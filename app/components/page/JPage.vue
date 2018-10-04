<template lang="pug">
    .columns
        .column
            h1.title {{ title }}
            page-message.mb4
            slot(v-if="!hasError")
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            default: ''
        }
    },
    computed: {
        ...mapGetters(['hasError']),
        ...mapGetters('account', ['loggedIn'])
    },
    methods: {
        // prevent guest from accessing guarded routes and set errors
        guard () {
            // check if the route needs auth or a user is logged in
            if (!this.$route.meta.auth || this.loggedIn) return

            this.$store.commit('setMessage', { 
                type: 'error', 
                comp: 'access-denied'
            })
        }
    },
    created () {
        this.guard()
    },
    activated () {
        this.guard()
    },
    updated () {
        this.guard()
    },
    mounted () {
        document.title = process.env.MIX_APP_NAME + (this.title ? ' - ' + this.title : '')
    }
}
</script>

