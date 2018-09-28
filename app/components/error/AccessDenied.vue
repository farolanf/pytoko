<template lang="pug">
    div
        template Silahkan 
        router-link.is-link(:to="loginUrl") masuk
        template &nbsp;untuk mengakses halaman ini
</template>

<script>
export default {
    computed: {
        loginUrl () {
            return {
                name: 'login', 
                query: { url: this.$route.fullPath }
            }
        }
    }
}
</script>

