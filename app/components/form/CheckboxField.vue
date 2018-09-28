<template lang="pug">
    .field
        .control
            label.checkbox
                input(type="checkbox")
                template {{ title }}
</template>

<script>
export default {
    props: {
        title: {
            type: String
        }
    }
}
</script>

