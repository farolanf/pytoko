import Vue from 'vue'
import Vuex from 'vuex'
import account from './account'
import request from './request'
import cache from './cache'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        account,
        request,
        cache,
    },
    state: {
        mobile: true,
        tablet: false,
        msgType: null,
        msg: null,
        msgComponent: null,
    },
    getters: {
        hasError (state) {
            return state.msgType === 'error'
        },
    },
    mutations: {
        setMedia (state, { mobile, tablet }) {
            state.mobile = mobile
            state.tablet = tablet
        },
        setMessage (state, { type = null, msg = '', comp = null } = {}) {
            state.msgType = type
            state.msg = msg
            state.msgComponent = comp
        },
        clearMessage (state) {
            state.msgType = null
            state.msg = null
            state.msgComponent = null
        },
    },
})

// handle user change
store.watch(state => state.account.user, () => {
    
    // clear page messages/errors (eg. access-denied)
    store.commit('clearMessage')
})

export default store