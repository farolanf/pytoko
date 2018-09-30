<template lang="pug">
    .navbar-item.has-dropdown(:class="{'is-active': profileDropdown}")
        a.navbar-link(:class="{'is-active': active}" @click.prevent="toggleProfile") Halo {{ user.username }}!
        .navbar-dropdown
            router-link.navbar-item(:to="{name: 'my-ads'}" @click.native="hideProfile") Iklan saya
            router-link.navbar-item(:to="{name: 'dashboard'}" exact @click.native="hideProfile") Akun
            a.navbar-item(@click="logout") Keluar
</template>

<script>
export default {
    data () {
        return {
            profileDropdown: false
        }
    },
    computed: {
        ...mapState('account', ['user']),
        active () {
            return this.$route.path.startsWith('/akun')
        }
    },
    methods: {
        ...mapActions('account', ['logout']),
        toggleProfile () {
            this.profileDropdown = !this.profileDropdown
        },
        hideProfile () {
            this.profileDropdown = false
        }
    },
}
</script>
