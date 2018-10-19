once(function imageUploads () {

    const events = new Vue()
    let cropper

    Vue.component('image-upload', {
        template: $('#image-upload-template').html(),
        props: ['item'],
        methods: {
            onCrop () {
                events.$emit('crop', this.item)
            },
            onRemove () {
                events.$emit('remove', this.item)
            }
        }
    })

    new Vue({
        el: document.querySelector('.image-uploads__container'),
        data: {
            imageUploads: DATA.imageUploads,
            currentItem: null,
        },
        methods: {
            saveCurrentItem (item) {
                this.currentItem = item
            },
            onRemove (item) {
                item.image = ''
            },
            onSave () {

            }
        },
        created () {
            events.$on('crop', this.saveCurrentItem)
            events.$on('remove', this.onRemove)
            events.$on('save', this.onSave)
        },
        mounted () {
            dragula([document.querySelector('.image-uploads__container')], {
                direction: 'horizontal'
            })
        }
    })

    new Vue({
        el: document.querySelector('.image-uploads__cropper-modal'),
        data: {
            visible: false,
        },
        methods: {
            show (item) {
                this.visible = true
                cropper = this.initCropper(item)
            },
            hide () {
                this.destroyCropper()
                this.visible = false
            },
            save () {
                events.$emit('save')
                this.hide()
            },
            rotateLeft () {
                cropper.rotate(-90)
            },
            rotateRight () {
                cropper.rotate(90)
            },
            initCropper (item) {
                this.$refs.img.src = item.image
                return new Cropper(this.$refs.img, {
                    rotatable: true,
                    viewMode: 2
                })
            },
            destroyCropper () {
                if (cropper) {
                    cropper.destroy()
                    cropper = null
                }
            }
        },
        created () {
            events.$on('crop', this.show)
        }
    })
})