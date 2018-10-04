<template lang="pug">
    div
        .notification.mt4(v-if="msgType" :class="cls")
            template(v-if="msg") {{ msg }}
            div(v-else-if="msgComponent" :is="msgComponent")
</template>

<script>
export default {
    computed: {
        ...mapState(['msgType', 'msg', 'msgComponent']),
        cls () {
            return this.msgType === 'error' ? 'is-danger' : 'is-info'
        }
    }
}
</script>
