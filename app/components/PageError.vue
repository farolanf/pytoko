<template lang="pug">
    div
        .notification.mt4(v-if="errorType" :class="errorClass")
            template(v-if="errorMsg") {{ errorMsg }}
            div(v-else-if="errorComp" :is="errorComp")
</template>

<script>
export default {
    computed: {
        ...mapState(['errorType', 'errorMsg', 'errorComp']),
        errorClass () {
            switch (this.errorType) {
                default:
                    return  'is-danger'
            }
        }
    }
}
</script>
