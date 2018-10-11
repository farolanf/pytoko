<template lang="pug">
    .box
        form(@submit.prevent="submit")
            .select
                select(v-model="category")
                    option(value="")
</template>

<script>
export default {
    methods: {
        submit () {

        }
    }
}
</script>

