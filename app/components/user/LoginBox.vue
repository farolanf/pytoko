<template lang="pug">
    div
        .notification.is-danger(v-if="message") {{ message }}
        
        form(@submit.prevent="login")
        
            input-field(type="email" name="email" title="Email" required left-icon="fa fa-envelope" placeholder="Alamat email" v-model="email" :error="hasError('email')" :error-msg="getError('email')")

            input-field(type="password" name="password" title="Password" required left-icon="fa fa-lock" placeholder="Password" v-model="password" :error="hasError('password')" :error-msg="getError('password')")

            .field.is-grouped
                .control
                    button.button.is-link(type="submit" :class="{'is-loading': loading}") Masuk
                .control
                    router-link.button.is-text(:to="{name: 'forgot-password'}") Lupa password
</template>

<script>
export default {
    data () {
        return {
            email: '',
            password: '',
            loading: false
        }
    },
    computed: {
        ...mapState('request', ['message']),
        ...mapGetters('request', ['hasError', 'getError']),
    },
    methods: {
        ...mapActions(['account/login']),
        login () {
            const { email, password } = this
            this.loading = true
            this['account/login']({ email, password })
                .then(() => {
                    this.$router.push(this.$route.query.url || { name: 'dashboard' })
                })
                .finally(() => {
                    this.loading = false
                })
        }
    }
}
</script>

