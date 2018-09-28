<template lang="pug">
    .mt4
        .notification(v-if="lastMessage" :class="{'is-danger': lastError, 'is-success': !lastError}") {{ lastMessage }}
        router-link(:to="{name: 'front'}") Kembali ke halaman utama
</template>

<script>
export default {
    data () {
        return {
            // cache last status so it can displayed when navigating back to this page
            lastMessage: '',
            lastError: false            
        }
    },
    computed: mapState('request', ['message', 'error', 'status']),
    methods: {
        init () {
            if (this.status !== null) {
                this.lastMessage = this.message
                this.lastError = this.error
            }
        }
    },
    created () {
        this.init()
    },
    activated () {
        this.init()
    }
}
</script>
