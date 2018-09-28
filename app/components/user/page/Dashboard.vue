<template lang="pug">
    j-page(title="Akun")
        pre {{ userJson }}
</template>

<script>
export default {
    computed: {
        ...mapState('account', ['user']),
        userJson () {
            return JSON.stringify(this.user, null, 4)
        }
    },
    methods: mapActions('account', ['getUser']),
    created () {
        // use getUser to demonstrate token refresh
        this.getUser()
    }
}
</script>

