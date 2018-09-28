<template lang="pug">
    div
        .notification.is-info Masukkan email anda untuk menerima link ke halaman reset password

        .notification(v-if="message" :class="{'is-danger': error, 'is-success': !error}") {{ message }}
        
        form(@submit.prevent="sendEmail")

            input-field(type="email" name="email" title="Email" required left-icon="fa fa-envelope" placeholder="Alamat email" v-model="email" :error="!!errors.email" :error-msg="errors.email")

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
    computed: mapState('request', ['message', 'errors', 'error']),
    methods: {
        ...mapMutations('request', ['resetRequestState']),
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

