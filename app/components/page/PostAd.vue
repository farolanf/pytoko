<template lang="pug">
    j-page.w-100.w-60-ns(title="Pasang Iklan")
        .columns
            .column
                
                form(@submit.prevent="submit")

                    .field
                        .label Kategori
                        .control.relative
                            category-picker(v-model="category")
                            input(type="hidden" name="category" :value="category")

                    input-field(name="title" title="Judul iklan" required placeholder="Judul iklan" v-model="title")

                    .field
                        .label Deskripsi iklan
                        .control
                            textarea.textarea(rows="10" cols="50" name="desc" v-model="desc")
                        p.help Terangkan produk/jasa dengan singkat dan jelas. Terangkan juga kekurangannya jika ada.

                    .field
                        .label Foto Produk
                        .control
                            image-uploads(:max="8" v-model="imageItems")
                        p.help Sertakan minimal 3 foto untuk menarik pembeli

                    .field
                        .label Provinsi
                        .control
                            .select
                                select(name="provinsi" v-model="provinsi" @change="onProvinsiChange" required)
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
export default {
    data () {
        return {
            category: null,
            title: '',
            desc: '',
            provinsi: 0,
            kabupaten: 0,
            imageItems: null,
            loading: false
        }
    },
    computed: {
        ...mapState('regions', ['provinsiMap']),
        ...mapState('regions', { dataProvinsi: 'provinsi' }),
        ...mapGetters('account', ['loggedIn']),
        selectedProvinsi () {
            return this.provinsi ? this.provinsiMap[this.provinsi] : null
        }
    },
    methods: {
        ...mapActions('regions', ['getProvinsi', 'getKabupaten']),
        submit (e) {
            const fd = new FormData(e.target)
            fd.append('nama', 'andi')
            fd.append('nama', 'budi')
            if (this.imageItems && this.imageItems.length) {
                this.imageItems.forEach((item, i) => {
                    fd.append(`images[${i}]`, item.blob, item.file.name)
                })
            }
            this.loading = true
            axios.post('/api/ads/', fd).then(() => {
                this.$router.push({ name: 'my-ads' })
            }).finally(() => {
                this.loading = false
            })
        },
        onProvinsiChange () {
            this.kabupaten = 0
            this.getKabupaten({ provinsiId: this.provinsi })
        }
    },
    mounted () {
        this.getProvinsi()
    }
}
</script>

