<template lang="pug">
    div
        .hero.is-danger.mt3
            .hero-body
                .container
                    .section
                        h1.title 404 - Halaman tidak ditemukan
                        h2.subtitle {{ href }}
                
        div.mt3
            router-link(:to="{name: 'front'}") Kembali ke halaman utama
</template>

<script>
export default {
    computed: {
        href () {
            return location.href
        }
    }
}
</script>

