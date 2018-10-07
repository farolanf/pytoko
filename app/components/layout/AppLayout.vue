<template lang="pug">
    #app-layout
        top-bar
        sticky-observer(target="#topbar" sticky-class="shadow-3")
        .main-content.container
            keep-alive(include="request-status-page")
                router-view
        footer.footer.mt4.absolute.bottom-0.w-100
            .container.static
                .columns
                    .column
                        a.is-link Kontak
                    .column
                        span.has-text-grey Hak cipta (C) 2018 juwal.com
        media-detector
</template>

<script>
export default {
}
</script>

<style lang="scss">
@import '~bulma/bulma';

#app-layout {
    padding-bottom: calc(168px + 4rem);
}
@include until($tablet) {
    #app-layout > .main-content {
        padding: 3rem .5rem 0 .5rem;
    }
}
@include from($tablet) {
    #app-layout > .main-content {
        padding: 3rem 0;
    }
}
</style>
