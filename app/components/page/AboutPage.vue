<template lang="pug">
    j-page(title="Tentang Kami")
        input(id="crop-image" type="file" accept="image/*" ref="file" @change="handleFile")
        button.button(@click="reset") Reset
        button.button(@click="show") Show cropper
        button.button(@click="hide") Close
        div.w-50
            img.mw-100(:src="img" ref="img")
</template>

<script>
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.min.css'

export default {
    data () {
        return {
            img: null
        }
    },
    watch: {
        img (val) {
            if (!val) return
            this.$nextTick(() => {
                this.cropper = new Cropper(this.$refs.img, {
                    viewMode: 3,
                    autoCrop: false
                })
            })
        }
    },
    methods: {
        show () {
            this.cropper.crop()
        },
        hide () {
            this.cropper.clear()
        },
        reset () {
            this.cropper.reset()
        },
        handleFile (e) {
            if (!e.target.files.length) return
            const reader = new FileReader();
            reader.onload = e => {
                this.img = e.target.result
            }
            reader.readAsDataURL(e.target.files[0])
        }
    }
}
</script>
