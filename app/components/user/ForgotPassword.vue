<template lang="pug">
    div
        .notification.is-info Masukkan email anda untuk menerima link ke halaman reset password

        error-messages
        
        form(@submit.prevent="sendEmail")

            input-field(type="email" name="email" title="Email" required left-icon="fa fa-envelope" placeholder="Alamat email" v-model="email" :error="hasError('email')" :error-msg="getError('email')")

            .field.is-grouped
                .control
                    button.button.is-link(type="submit" :class="{'is-loading': loading}") Kirim email
                .control
                    router-link.button.is-text(:to="{name: 'login'}") Masuk
</template>

<script>
export default {
    data () {
        return {
            email: '',
            loading: false
        }
    },
    computed: mapGetters('request', ['hasError', 'getError']),
    methods: {
        ...mapActions('account', ['sendResetPasswordEmail']),
        sendEmail () {
            const { email } = this
            this.loading = true
            this.sendResetPasswordEmail({ email })
                .then(() => {
                    this.$router.push({ name: 'request-status' })
                })
                .finally(() => {
                    this.loading = false
                    this.email = ''
                })
        }
    }
}
</script>

