<template lang="pug">
    p.help.is-danger(v-if="hasError(name)") {{ getError(name) }}
</template>

<script>
export default {
    props: {
        name: {
            type: String,
            required: true
        }
    },
    computed: mapGetters('request', ['hasError', 'getError'])
}
</script>
