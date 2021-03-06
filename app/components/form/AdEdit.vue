<template lang="pug">
    form(@submit.prevent="submit")

        form-field.relative(title="Kategori" name="category")
            category-picker(v-model="category")
            input(type="hidden" name="category" :value="category")

        input-field(name="title" title="Judul iklan" required placeholder="Judul iklan" maxlength="70" :help="(70 - title.length) + ' karakter tersisa.'" v-model="title")

        .field
            .label Harga
            .control.flex.items-center

                input.input.w-50.tr(v-if="mobile" name="price" type="number" required placeholder="123456" max="999999999999" v-model="price")

                input.input.w-20.tr(v-if="tablet" name="price" type="number" required placeholder="123456" max="999999999999" v-model="price")

                label.checkbox.ml2
                    input(name="nego" type="checkbox" v-model="nego")
                    template &nbsp;Bisa nego

        form-field(title="Deskripsi iklan" name="desc" :help="'Terangkan produk/jasa dengan singkat dan jelas. Terangkan juga kekurangannya jika ada.<br>' + (4000 - desc.length) + ' karakter tersisa.'")
            textarea.textarea(v-error="" rows="10" cols="50" name="desc" maxlength="4000" v-model="desc")

        form-field(title="Foto Produk" name="images" help="Sertakan minimal 3 foto untuk menarik pembeli")
            image-uploads(v-error="images" :max="8" v-model="imageItems")

        .field
            .label Provinsi
            .control
                .select
                    select(name="provinsi" v-model="provinsi" required)
                        option(v-for="prov in dataProvinsi" :key="prov.id" :value="prov.id") {{ prov.name }}
                p.help Lokasi produk/jasa

        .field(v-if="provinsi")
            .label Kabupaten
            .control
                .select(v-if="selectedProvinsi && selectedProvinsi.kabupaten")
                    select(name="kabupaten" v-model="kabupaten" required)
                        option(v-for="kab, id in selectedProvinsi.kabupaten" :key="kab.id" :value="kab.id") {{ kab.name }}
                template(v-else)
                    button.button.is-text.is-loading
                p.help Lokasi produk/jasa
        
        .field.is-grouped
            .control
                button.button.is-link(type="submit" :class="{'is-loading': loading}") Simpan
</template>

<script>
import { updateFromResponse, updateFromError } from '#/store/request'
import { scrollToError } from '#/utils/dom'
import info from '@/mixins/info'

export default {
    mixins: [info],
    props: ['id'],
    data () {
        return {
            category: null,
            provinsi: null,
            kabupaten: null,
            title: '',
            desc: '',
            price: null,
            nego: true,
            images: null,
            imageItems: null,
            loading: false
        }
    },
    computed: {
        ...mapState('cache', ['provinsiMap']),
        ...mapState('cache', { dataProvinsi: 'provinsi' }),
        ...mapGetters('account', ['loggedIn']),
        selectedProvinsi () {
            return this.provinsi ? this.provinsiMap[this.provinsi] : null
        },
        exists () {
            return !!this.id
        },
        url () {
            return this.exists ? `/api/ads/${this.id}/` : '/api/ads/'
        }
    },
    watch: {
        provinsi (val) {
            !this.exists && this.$emit('update:kabupaten', 0)
            this.getKabupaten({ provinsiId: val })
        }
    },
    methods: {
        ...mapActions('cache', ['getProvinsi', 'getKabupaten']),
        submit (e) {
            const fd = new FormData(e.target)
            if (this.imageItems && this.imageItems.length) {
                this.imageItems.forEach((item, i) => {
                    if (item.blob) {
                        const name = item.file ? item.file.name : item.name
                        fd.append(`images[${i}]`, item.blob, name)
                    }
                })
            }
            this.loading = true
            const method = this.exists ? 'put' : 'post'
            axios[method](this.url, fd).then(() => {
                this.$router.push({ name: 'my-ads' })
            }).then(updateFromResponse)
                .catch(updateFromError)
                .catch(scrollToError)
                .finally(() => {
                    this.loading = false
                })
        },
        kabupatenChange (e) {
            this.$emit('update:kabupaten', e.target.value)            
        },
        load (id) {
            this.loading = true
            axios.get(`/api/ads/${id}/`).then(resp => {
                Object.assign(this, _.pick(resp.data, ['category', 'provinsi', 'kabupaten', 'title', 'desc', 'price', 'images']))
                
                // load images
                if (this.images) {
                    this.imageItems = this.images.map(item => ({ url: item.image }))
                }
            }).finally(() => {
                this.loading = false
            })
        }
    },
    created (){
        if (this.id) {
            this.load(this.id)
        }
    },
    mounted () {
        this.getProvinsi()
    }
}
</script>

