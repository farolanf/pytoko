<template lang="pug">
    .image-uploads-item.pointer.relative.hide-child.mr2.mb2.h4.w4.bw1.ba.b--near-white

        .overflow-hidden.w-100.h-100(v-if="img")
    
            img.w-100(:src="img")
    
        .flex.justify-center.items-center.bg-washed-blue.bw1.b--dotted.b--light-silver.w4.h4.mr2.mb2(v-else @click="browse")
            span.icon
                i.fa.fa-plus-square.f3

        .child.bg-black-40.absolute.absolute--fill.image-uploads-item__drag-handle.move(v-if="img")
            span.icon.absolute.top--05.right--05.bg-red.br-100.grow.pointer(@click.prevent="del")
                i.fa.fa-remove.f4.white
            span.icon.absolute.top--05.left--05.br-100.grow.has-background-link.pointer(@click="$emit('edit')")
                i.fa.fa-crop.f4.white

        input.dn(type="file" accept="image/*" ref="file" @change="handleFile")
</template>

<script>
export default {
    props: ['img'],
    methods: {
        browse () {
            this.$refs.file.click()
        },
        del () {
            this.$refs.file.value = null
            this.$emit('image', null)
        },
        handleFile (e) {
            if (!e.target.files.length) return

            this.$emit('file', e.target.files[0])
            
            const reader = new FileReader();
            reader.onload = e => {
                this.$emit('image', e.target.result)
            }
            reader.readAsDataURL(e.target.files[0])
        }
    }
}
</script>

<style lang="stylus">
.image-uploads-item
    .img-container
        overflow hidden
</style>
