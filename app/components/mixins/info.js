import { categoryPathStr } from '#/utils/data'

export default {
    computed: {
        ...mapState(['mobile', 'tablet']),
        ...mapState('cache', ['categoryPaths', 'provinsiMap', 'kabupatenMap']),
    },
    methods: {
        ...mapActions('cache', ['getCategory', 'getProvinsi', 'getKabupaten']),
        categoryPathStr (categoryId) {
            return categoryPathStr(this.categoryPaths[categoryId])
        },
        provinsiStr (provinsiId) {
            return this.provinsiMap[provinsiId] ? this.provinsiMap[provinsiId].name : ''
        },
        kabupatenStr (provinsiId, kabupatenId) {
            if (!this.kabupatenMap[kabupatenId]) {
                this.getKabupaten({ provinsiId })
                return
            }
            return this.kabupatenMap[kabupatenId] ? this.kabupatenMap[kabupatenId].name : ''
        }
    },
    mounted () {
        this.getCategory()
        this.getProvinsi()
    }
}