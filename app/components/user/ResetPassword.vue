<template lang="pug">
    div
        .notification.is-danger(v-if="hasError('non_field_errors')")
            p {{ getError('non_field_errors') }}
            p {{ getError('token') }}
        
        form(@submit.prevent="submit" ref="form")

            input-field(type="password" name="password" title="Password" required left-icon="fa fa-lock" v-model="password" :error="hasError('password')" :error-msg="getError('password')" @change="validatePassword")

            input-field(type="password" name="password_confirm" title="Ulang password" required left-icon="fa fa-lock" v-model="passwordConfirm" :error="hasError('password_confirm')" :error-msg="getError('password_confirm')" @change="validatePassword")

            .field
                .control
                    button.button.is-link(type="submit" :class="{'is-loading': loading}") Simpan
</template>

<script>
export default {
    data () {
        return {
            loading: false,
            password: '',
            passwordConfirm: ''
        }
    },
    computed: mapGetters('request', ['hasError', 'getError']),
    methods: {
        ...mapActions('account', ['resetPassword']),
        validatePassword () {
            const passwordConfirm = this.$el.querySelector('[name="password_confirm"]')
            let error = ''
            if (this.passwordConfirm && this.passwordConfirm !== this.password) {
                error = 'Kedua password harus sama'
            }
            passwordConfirm.setCustomValidity(error)
        },
        validate () {
            return this.$refs.form.reportValidity()
        },
        submit () {
            if (!this.validate()) return
            this.loading = true
            this.resetPassword({
                token: this.$route.query.t,
                password: this.password,
                passwordConfirm: this.passwordConfirm
            }).then(() => {
                this.$router.push({ name: 'request-status' })
            }).finally(() => {
                this.loading = false
            })
        }
    }
}
</script>

