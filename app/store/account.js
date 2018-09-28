import axios from "axios";
import { removeToken } from '../helpers/account'
import { updateFromResponse, updateFromError } from './request'

export default {
    namespaced: true,
    state: {
        user: null
    },
    getters: {
        loggedIn (state) {
            return !!state.user 
        }
    },
    mutations: {
        setUser (state, { user } = {}) {
            state.user = user
        }
    },
    actions: {
        getUser ({ commit }) {
            return axios.get('/api/user')
                .then(resp => {
                    commit('setUser', { user: resp.data })
                })
        },
        login ({ commit }, { email, password }) {
            return axios.post('/api/login', { email, password })
                .then(updateFromResponse)
                .catch(updateFromError)
                .then(resp => {
                    commit('setUser', { user: resp.data.user })
                    return resp
                })
        },
        logout ({ commit }) {
            removeToken()
            commit('setUser')
        },
        sendResetPasswordEmail ({ commit }, { email }) {
            return axios.post('/api/password/email', { email })
                .then(updateFromResponse)
                .catch(updateFromError)
        }
    }
}