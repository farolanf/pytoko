<template lang="pug">
    .notification.is-danger(v-if="error && messages.length")
        p(v-for="msg in messages") {{ msg }}
</template>

<script>
export default {
    props: {
        name: {
            type: [Array, String],
            default: 'non_field_errors'
        },
        withDefault: {
            type: Boolean
        },
        message: {
            type: String,
            default: ''
        }
    },
    computed: {
        ...mapState('request', ['error']),
        ...mapGetters('request', ['hasError', 'getError']),
        messages () {
            const names = Array.isArray(this.name) 
                ? this.name 
                : this.name ? [this.name] : []
            this.withDefault && names.unshift('non_field_errors')
            return names.reduce((arr, name) => {
                arr = arr.concat(this.getError(name, true))
                return arr
            }, this.message ? [this.message] : [])
        }
    }
}
</script>
