<template lang="pug">
    nav#topbar.navbar.is-primary
        .container
            .navbar-brand
                a.navbar-item(href="/") Juwal
                a.navbar-burger(:class="{'is-active': show}" @click="show = !show")
                    span
                    span
                    span

            .navbar-menu(:class="{'is-active': show}")
                .navbar-start
                    router-link.navbar-item(:to="{name: 'front'}" exact) Depan
                    router-link.navbar-item(:to="{name: 'about'}") Tentang kami
                
                .navbar-end
                    router-link.navbar-item(:to="{name: 'post-ad'}") Pasang iklan

                    template(v-if="!user")
                        router-link.navbar-item(:to="{name: 'login'}") Masuk
                        router-link.navbar-item(:to="{name: 'daftar'}") Daftar

                    template(v-else)
                        profile-dropdown
</template>

<script>
export default {
    data () {
        return {
            show: false
        }
    },
    computed: mapState('account', ['user'])
}
</script>

<style lang="stylus">
#topbar
    position sticky
    top 0
    transition all .1s
</style>


