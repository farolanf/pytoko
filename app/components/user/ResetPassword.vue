<template lang="pug">
    div
        .notification(v-if="message" :class="{'is-danger': error, 'is-success': !error}") {{ message }}
        
        form(@submit.prevent="submit" ref="form")

            input-field(type="password" name="password" title="Password" required left-icon="fa fa-lock" v-model="password" :error="!!errors.password" :error-msg="errors.password" @change="validatePassword")

            input-field(type="password" name="password_confirm" title="Ulang password" required left-icon="fa fa-lock" v-model="passwordConfirm" :error="!!errors.password_confirm" :error-msg="errors.password_confirm" @change="validatePassword")

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
    computed: mapState('request', ['message', 'errors', 'error']),
    methods: {
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
        resetPassword () {
            axios.post('/api/password/reset/', {
                token: this.$route.query.t,
                password: this.password,
                password_confirm: this.passwordConfirm
            })
        },
        submit () {
            if (this.validate()) {
                this.resetPassword()
            }
        }
    }
}
</script>

