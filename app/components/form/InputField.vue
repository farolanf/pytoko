<template lang="pug">
    form-field(errorIcon v-bind="{title, name, leftIcon, help, errorMsg, successMsg, error, success}")
        field-input(v-bind="attrs" @input="$emit('input', $event)" @change="$emit('change', $event)")
</template>

<script>
export default {
    inheritAttrs: false,
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
        title: {
            type: String
        },
        leftIcon: {
            type: String
        },
        placeholder: {
            type: String
        },
        required: {
            type: Boolean
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
        attrs () {
            return { 
                ..._.pick(this, ['type', 'value', 'name', 'placeholder', 'required', 'error', 'sucess']),
                ...this.$attrs 
            }            
        }

    }
}
</script>
