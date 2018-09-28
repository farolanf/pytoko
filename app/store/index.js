import Vue from 'vue'
import Vuex from 'vuex'
import account from './account'
import request from './request'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        account,
        request
    },
    state: {
        errorType: null,
        errorMsg: null,
        errorComp: null
    },
    getters: {
        hasError (state) {
            return !!state.errorType
        }
    },
    mutations: {
        setError (state, { type = null, msg = '', comp = null } = {}) {
            state.errorType = type
            state.errorMsg = msg
            state.errorComp = comp
        },
        clearError (state) {
            state.errorType = null
            state.errorMsg = null
            state.errorComp = null
        }
    }
})

// handle user change
store.watch(state => state.account.user, () => {
    
    // clear page errors (eg. access-denied)
    store.commit('setError')
})

export default store