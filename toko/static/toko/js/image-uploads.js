once(function imageUploads () {

    const events = new Vue()
    let cropper

    DATA.imageUploads.forEach((item, i) => {
        if (item.file) {
            item.name = utils.lastSegment(item.file)
        }
        if (!item.id) {
            item.id = Date.now() + i
        }
        item.originalFile = item.file
    })

    Vue.component('image-upload', {
        template: $('#image-upload-template').html(),
        props: ['item', 'index'],
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
                const list = this.imageUploads.filter(item => item.file)
                    .concat(this.imageUploads.filter(item => !item.file))
                const args = [0, this.imageUploads.length].concat(list)
                this.imageUploads.splice.apply(this.imageUploads, args)
            },
            onBrowse () {
                // use first empty slot
                this.imageUploads.find(item => {
                    if (!item.file) {
                        events.$emit('do browse', item)
                        return true
                    }
                })
            },
            onRemove (item) {
                item.file = ''
                this.sort()
            },
            onLoadFile ({ name, dataUrl, item }) {
                this.$set(item, 'file', dataUrl)
                this.$set(item, 'name', name)
            },
            onSave () {
                const dataUrl = cropper.getCroppedCanvas().toDataURL()
                this.$set(this.currentItem, 'file', dataUrl)
            }
        },
        created () {
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
                    return (prevItem && prevItem.file) || (nextItem && nextItem.file)
                }
            })
            drake.on('drop', () => {
                const list = []
                $('.image-upload', this.$el).each((i, el) => {
                    const item = this.getItem(+$(el).attr('data-id'))
                    list.push(item)
                })
                const args = [0, this.imageUploads.length].concat(list)
                this.imageUploads.splice.apply(this.imageUploads, args)
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
                this.$refs.img.src = item.file
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