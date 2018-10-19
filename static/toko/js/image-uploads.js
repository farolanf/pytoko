once(function imageUploads () {

    const events = new Vue()
    let cropper

    Vue.component('image-upload', {
        template: $('#image-upload-template').html(),
        props: ['item'],
        methods: {
            browse (item) {
                if (item.id !== this.item.id) return
                this.$refs.file.click()
            },
            onBrowse () {
                events.$emit('browse')
            },
            onCrop () {
                events.$emit('crop', this.item)
            },
            onRemove () {
                events.$emit('remove', this.item)
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
        },
        created () {
            events.$on('do browse', this.browse)
        }
    })

    new Vue({
        el: document.querySelector('.image-uploads__container'),
        data: {
            imageUploads: DATA.imageUploads,
            currentItem: null,
        },
        methods: {
            onBrowse () {
                // use first empty slot
                this.imageUploads.find(item => {
                    if (!item.image) {
                        events.$emit('do browse', item)
                        return true
                    }
                })
            },
            saveCurrentItem (item) {
                this.currentItem = item
            },
            onRemove (item) {
                item.image = ''
            },
            onSave () {

            },
            initData () {
                this.imageUploads.forEach((item, i) => {
                    if (!item.id) {
                        this.$set(item, 'id', Date.now() + i)
                    }
                })
            }
        },
        created () {
            this.initData()
            events.$on('crop', this.saveCurrentItem)
            events.$on('browse', this.onBrowse)
            events.$on('remove', this.onRemove)
            events.$on('save', this.onSave)
        },
        mounted () {
            dragula([document.querySelector('.image-uploads__container')], {
                direction: 'horizontal',
                moves (el, src, handle) {
                    return $(handle).is('[data-move-handle]')
                }
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