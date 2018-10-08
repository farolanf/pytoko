<template lang="pug">
    span(:is="tag")
        span.icon(v-if="loading")
            i.fa.fa-spinner.fa-pulse
        template(v-else)
            template {{ text }}
            slot
</template>

<script>
export default {
    props: {
        loading: {
            type: Boolean
        },
        text: {
            type: String
        },
        tag: {
            type: String,
            default: 'span'
        }
    }
}
</script>

