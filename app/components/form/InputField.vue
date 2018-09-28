<template lang="pug">
    .field
        .label {{ title }}
        
        .control.has-icons-right(:class="{'has-icons-left': leftIcon}")
            
            input.input(:class="{'is-danger': error, 'is-success': success}" v-bind="{type, name, placeholder, required}" :value="value" @input="$emit('input', $event.target.value)")
            
            span.icon.is-small.is-left(v-if="leftIcon")
                i(:class="leftIcon")
            
            span.icon.is-small.is-right(v-if="error || success")
                i.fa.fa-exclamation-triangle(v-if="error")
                i.fa.fa-check(v-if="success")

            p.help.is-danger(v-if="error") {{ errorStr }}
            p.help.is-success(v-else-if="success") {{ successStr }}
            p.help(v-else-if="help") {{ help }}
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
        errorStr: {
            type: String
        },
        successStr: {
            type: String
        },
        error: {
            type: Boolean
        },
        success: {
            type: Boolean
        }
    }
}
</script>

