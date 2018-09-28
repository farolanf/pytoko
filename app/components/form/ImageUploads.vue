<template lang="pug">
    .image-uploads

        .image-uploads-container.flex.flex-wrap

            image-uploads-item(v-for="item in items" :key="item.id" :data-id="item.id" :id="`image-uploads-item-${item.id}`" :img="item.img" @file="file(item.id, $event)" @image="image(item.id, $event)" @edit="edit(item.id)")

        .modal(:class="{'is-active': cropperVisible}")
            .modal-background
            .modal-card
                header.modal-card-head
                    p.modal-card-title Pilih bagian terbaik dari gambar
                    a.delete(@click="cropperVisible = false")
                section.modal-card-body.flex(v-if="cropperItem")
                    img.mw-100(:src="cropperItem.originalImg" ref="img")
                footer.modal-card-foot
                    a.button.is-link(@click="save") Simpan
                    a.button(@click="cropperVisible = false") Batal
                    a.button(@click="rotateLeft")
                        span.icon
                            i.fa.fa-rotate-left
                    a.button(@click="rotateRight") 
                        span.icon
                            i.fa.fa-rotate-right
</template>

<script>
import 'cropperjs/dist/cropper.min.css'
import Cropper from 'cropperjs'

import 'dragula/dist/dragula.min.css'
import dragula from 'dragula'

export default {
    props: {
        max: {
            type: Number,
            default: 5
        }
    },
    data () {
        return {
            cropperVisible: false,
            cropperItem: null,
            items: Array(this.max).fill({})
                .map((item, i) => ({ id: i }))
        }
    },
    watch: {
        cropperVisible (val) {
            if (!val) {
                this.cropperItem = null
            }
        }
    },
    methods: {
        rotateLeft () {
            this.cropperItem.cropper.rotate(-90);
        },
        rotateRight () {
            this.cropperItem.cropper.rotate(90);
        },
        save () {
            this.cropperItem.cropperData = this.cropperItem.cropper.getData()
            this.cropperItem.cropper.getCroppedCanvas().toBlob(blob => {
                this.cropperItem.blob = blob
                this.cropperItem.img = URL.createObjectURL(blob)
                this.cropperVisible = false
                this.emitChange()
            })
        },
        edit (id) {
            const item = this.getItem(id)
            if (item.cropper) {
                item.cropper.destroy()
            }
            this.cropperItem = item
            this.cropperVisible = true
            this.$nextTick(() => {
                this.cropperItem.cropper = new Cropper(this.$refs.img, {
                    rotatable: true,
                    ready: () => {
                        this.cropperItem.cropperData && this.cropperItem.cropper.setData(this.cropperItem.cropperData)
                    }
                })
            })
        },
        async image (id, img) {
            const item = this.getItem(id)
            item.blob = await fetch(img).then(r => r.blob()) 
            item.originalImg = img
            this.$set(item, 'img', img)
            this.sort()
            this.emitChange()
        },
        file (id, file) {
            this.getItem(id).file = file
        },
        getItem (id) {
            return this.items.find(item => item.id === id)
        },
        sort () {
            this.items = this.items.filter(item => item.img).concat(
                this.items.filter(item => !item.img)
            )
        },
        emitChange () {
            const items = this.items.filter(item => item.blob)
                .map(item => ({
                    file: item.file,
                    blob: item.blob
                }))
            this.$emit('input', items)
        },
        initDrag () {
            this.drake = dragula([this.$el.querySelector('.image-uploads-container')], {
                direction: 'horizontal',
                moves (el, src, handle, sibling) {
                    return handle.classList.contains('image-uploads-item__drag-handle') && dropOnImage(el, sibling)
                },
                accepts (el, target, src, sibling) {
                    return dropOnImage(el, sibling)
                }            
            })
            this.drake.on('drop', (el, target, src, sibling) => {
                // sync items order
                const items = []
                Array.from(target.children).forEach(el => {
                    const id = +el.getAttribute('data-id')
                    const i = this.items.findIndex(item => item.id === id)
                    items.push(this.items[i])
                })
                this.items = items
                this.emitChange()
            })
            function dropOnImage (el, sibling) {
                let replaceEl = sibling ? (sibling.previousSibling || sibling)
                    : el.parentNode.children.item(el.parentNode.children.length - 1)
                return replaceEl.querySelector('input[type="file"]').value
            }
        }
    },
    mounted () {
        this.initDrag()
    },
    beforeDestroy () {
        if (this.drake) {
            this.drake.destroy()
        }
    }
}
</script>

<style lang="stylus">
</style>
