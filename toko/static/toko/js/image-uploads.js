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
    
                const name = e.target.files[0].name

                const reader = new FileReader();
                reader.onload = e => {
                    events.$emit('load', {
                        name,
                        dataUrl: e.target.result, 
                        item: this.item
                    })
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
            saveCurrentItem (item) {
                this.currentItem = item
            },
            getItem (id) {
                return this.imageUploads.find(item => item.id === id)
            },
            sort () {
                this.imageUploads = this.imageUploads.filter(item => item.image)
                    .concat(this.imageUploads.filter(item => !item.image))
            },
            onBrowse () {
                // use first empty slot
                this.imageUploads.find(item => {
                    if (!item.image) {
                        events.$emit('do browse', item)
                        return true
                    }
                })
            },
            onRemove (item) {
                item.image = ''
                this.sort()
            },
            onLoadFile ({ name, dataUrl, item }) {
                this.$set(item, 'image', dataUrl)
                this.$set(item, 'name', name)
            },
            onSave () {
                const dataUrl = cropper.getCroppedCanvas().toDataURL()
                this.$set(this.currentItem, 'image', dataUrl)
            },
            initData () {
                this.imageUploads.forEach((item, i) => {
                    item.image && this.$set(item, 'name', utils.lastSegment(item.image))
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
            events.$on('load', this.onLoadFile)
            events.$on('save', this.onSave)
        },
        mounted () {
            const drake = dragula([document.querySelector('.image-uploads__container')], {
                direction: 'horizontal',
                moves: (el, src, handle) => {
                    return $(handle).is('[data-move-handle]')
                },
                accepts: (el, target, src, sibling) => {
                    const prev = sibling ? sibling.previousSibling : null
                    const next = sibling || target.children[target.children.length - 1]
                    const prevItem = this.getItem(+$(prev).attr('data-id'))
                    const nextItem = this.getItem(+$(next).attr('data-id'))
                    return (prevItem && prevItem.image) || (nextItem && nextItem.image)
                }
            })
            drake.on('drop', () => {
                const list = []
                $('.image-upload', this.$el).each((i, el) => {
                    const item = this.getItem(+$(el).attr('data-id'))
                    list.push(item)
                })
                this.imageUploads = list
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