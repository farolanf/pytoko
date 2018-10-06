import Vue from 'vue'

export default {
    namespaced: true,
    state: {
        category: [],
        provinsi: [],
        kabupaten: [],
        categoryMap: {},
        provinsiMap: {},
        kabupatenMap: {},
    },
    mutations: {
        setCategory (state, { category, categoryMap }) {
            state.category = category
            state.categoryMap = categoryMap
        },
        setProvinsi (state, { provinsi, provinsiMap }) {
            state.provinsi = provinsi
            state.provinsiMap = provinsiMap
        },
        setKabupaten (state, { kabupaten, provinsiId }) {
            Vue.set(state.provinsiMap[provinsiId], 'kabupaten', kabupaten)
            kabupaten.forEach(item => {
                Vue.set(state.kabupatenMap, item.id, item)
            })
        },
    },
    actions: {
        getCategory ({ commit, state }) {
            if (state.category.length) return
            return axios.get('/api/taxonomy/category/')
                .then(resp => {
                    commit('setCategory', { 
                        category: resp.data,
                        categoryMap: mapFromTree(resp.data),
                    })
                })
        },
        getProvinsi ({ commit, state }) {
            if (state.provinsi.length) return
            return axios.get('/api/regions/provinsi/')
                .then(resp => {
                    commit('setProvinsi', { 
                        provinsi: resp.data,
                        provinsiMap: map(resp.data),
                    })
                })
        },
        getKabupaten ({ commit, state }, { provinsiId }) {
            if (state.provinsiMap[provinsiId].kabupaten) return
            return axios.get('/api/regions/kabupaten/', {
                params: {
                    provinsi_id: provinsiId
                }
            }).then(resp => {
                commit('setKabupaten', {
                    kabupaten: resp.data,
                    provinsiId,
                })
            })
        }
    }
}

function mapFromTree (data) {
    const map = {}
    data.length && traverseCategory(data[0], item => {
        map[item.id] = item
    })
    return map
    
    function traverseCategory (item, cb) {
        cb(item)
        item.children && item.children.forEach(item => {
            traverseCategory(item, cb)
        })
    }
}

function map (data) {
    return data.reduce((map, item) => {
        map[item.id] = item
        return map
    }, {})
}