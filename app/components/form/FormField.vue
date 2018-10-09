<template lang="pug">
    .field
        .label {{ title }}
        
        .control(:class="{'has-icons-left': leftIcon, 'has-icons-right': errorIcon}")

            slot
            
            span.icon.is-small.is-left(v-if="leftIcon")
                i(:class="leftIcon")
            
            span.icon.is-small.is-right(v-if="(_error && errorIcon) || success")
                i.fa.fa-exclamation-triangle(v-if="_error && errorIcon")
                i.fa.fa-check(v-if="success")

            p.help.is-danger(v-if="_error") {{ _errorMsg }}
            p.help.is-success(v-else-if="success") {{ successMsg }}
            p.help(v-if="help") {{ help }}
</template>

<script>
export default {
    props: {
        title: {
            type: String
        },
        name: {
            type: String
        },
        leftIcon: {
            type: String
        },
        errorIcon: {
        },
        help: {
            type: String
        },
        errorMsg: {
            type: String
        },
        successMsg: {
            type: String
        },
        error: {
            type: Boolean
        },
        success: {
            type: Boolean
        }
    },
    computed: {
        ...mapGetters('request', ['hasError', 'getError']),
        _error () {
            return this.error || this.hasError(this.name)
        },
        _errorMsg () {
            return this.errorMsg || this.getError(this.name)
        }
    }
}
</script>

