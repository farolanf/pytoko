import axios from "axios";
import { updateFromResponse, updateFromError } from './request'
import { saveJwtToken, removeJwtToken, getJwtPayload } from "../helpers/account";

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
            const payload = getJwtPayload()
            if (!payload) return
            return axios.get(`/api/users/${payload.user_id}/`)
                .then(resp => {
                    commit('setUser', { user: resp.data })
                })
        },
        login ({ commit, dispatch }, { email, password }) {
            return axios.post('/api-token-auth/', { email, password })
                .then(updateFromResponse)
                .then(resp => {
                    saveJwtToken(resp.data.token)
                    dispatch('getUser')
                    return resp
                })
                .catch(updateFromError)
            },
        logout ({ commit }) {
            removeJwtToken()
            commit('setUser')
        },
        sendResetPasswordEmail ({ commit }, { email }) {
            return axios.post('/api/password/email', { email })
                .then(updateFromResponse)
                .catch(updateFromError)
        }
    }
}