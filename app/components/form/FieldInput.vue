<template lang="pug">
    input.input(:class="{'is-danger': _error, 'is-success': success}" v-bind="attrs" :value="value" @input="$emit('input', $event.target.value)" @change="$emit('change', $event)")
</template>

<script>
export default {
    props: {
        value: {
            type: String
        },
        type: {
            type: String,
            default: 'text'
        },
        name: {
            type: String
        },
        placeholder: {
            type: String
        },
        required: {
            type: Boolean
        },
        error: {
            type: Boolean
        },
        success: {
            type: Boolean
        }
    },
    computed: {
        ...mapGetters('request', ['hasError']),
        _error () {
            return this.error || this.hasError(this.name)
        },
        attrs () {
            return { 
                ..._.pick(this, ['type', 'name', 'placeholder', 'required']),
                ...this.$attrs 
            }            
        }
    }
}
</script>

