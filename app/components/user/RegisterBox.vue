<template lang="pug">
    div
        .notification.is-danger(v-if="message") {{ message }}
        
        form(@submit.prevent="submit")
        
            input-field(type="email" name="email" title="Email" required left-icon="fa fa-envelope" placeholder="Alamat email" v-model="email" :error="hasError('email')" :error-msg="getError('email')")

            input-field(type="passowrd" name="password" title="Password" required left-icon="fa fa-lock" placeholder="Password" v-model="password" :error="hasError('password')" :error-msg="getError('password')")

            input-field(type="passowrd" name="password_confirm" title="Ulang password" required left-icon="fa fa-lock" placeholder="Password lagi" v-model="passwordConfirm" :error="hasError('password_confirm')" :error-msg="getError('password_confirm')")

            .field.is-grouped
                .control
                    button.button.is-link(type="submit" :class="{'is-loading': loading}") Daftar
                .control
                    router-link.button.is-text(:to="{name: 'login'}") Masuk
</template>

<script>
export default {
    data () {
        return {
            email: '',
            password: '',
            passwordConfirm: '',
            loading: false
        }
    },
    computed: {
        ...mapState('request', ['message']),
        ...mapGetters('request', ['hasError', 'getError']),
    },
    methods: {
        ...mapActions(['account/register', 'account/login']),
        submit () {
            const { email, password, passwordConfirm } = this
            this.loading = true
            this['account/register']({ email, password, passwordConfirm })
                .then(() => {
                    this.$router.push({ name: 'request-status' })
                })
                .finally(() => {
                    this.loading = false
                })
        }
    }
}
</script>

