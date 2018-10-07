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
        categoryPaths: {},
    },
    getters: {
        // get category path excluding the root
        getCategoryPathIds: state => id => 
            state.categoryPaths[id].map(item => item.id).slice(1)
    },
    mutations: {
        setCategory (state, { category, categoryMap, categoryPaths }) {
            state.category = category
            state.categoryMap = categoryMap
            state.categoryPaths = categoryPaths
        },
        setProvinsi (state, { provinsi, provinsiMap }) {
            state.provinsi = provinsi
            state.provinsiMap = provinsiMap
        },
        setKabupaten (state, { kabupaten, provinsiId }) {
            state.kabupaten = state.kabupaten.concat(kabupaten)
            kabupaten.forEach(item => {
                Vue.set(state.kabupatenMap, item.id, item)
            })
            Vue.set(state.provinsiMap[provinsiId], 'kabupaten', kabupaten)
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
                        categoryPaths: paths(resp.data),
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
            if (!state.provinsiMap[provinsiId] || state.provinsiMap[provinsiId].kabupaten) return
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

function walkTree (item, cb) {
    if (Array.isArray(item)) {
        item.forEach(item => walkTree(item, cb))
    } else {
        cb(item)
        Array.isArray(item.children) && walkTree(item.children, cb)
    }
}

function mapFromTree (data) {
    const map = {}
    walkTree(data, item => {
        item.isLeaf = !item.children || !item.children.length
        map[item.id] = item
    })
    return map
}

function map (data) {
    return data.reduce((map, item) => {
        map[item.id] = item
        return map
    }, {})
}

/**
 * Create path for each leaf in the tree.
 * 
 * @param {Object} tree 
 * @returns {Object} map of ID to path (array of IDs)
 */
function paths(tree) {
    let isRoot = !Array.isArray(tree)
    if (!isRoot) {
        tree = { children: tree }
    }
    const map = {}
    const stack = []
    let state = {
        item: tree,
        i: 0,
    }
    do {
        if (state.item.children && state.item.children.length 
                && state.i < state.item.children.length) {
            stack.push(state)
            state = {
                item: state.item.children[state.i++],
                i: 0,
            }
            if (!state.item.children || !state.item.children.length) {
                stack.push(state)
                map[state.item.id] = stack.map(state => state.item)
                !isRoot && map[state.item.id].shift()
                stack.pop()
            }
        } else {
            state = stack.pop()
        }
    } while (state)
    return map
}