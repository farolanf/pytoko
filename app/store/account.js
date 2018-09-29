import axios from "axios";
import { updateFromResponse, updateFromError } from './request'
import { saveJwtToken, removeJwtToken } from "../helpers/account";

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
            return axios.get('/user/')
                .then(resp => {
                    commit('setUser', { user: resp.data })
                })
        },
        login ({ commit }, { email, password }) {
            return axios.post('/api-token-auth/', { email, password })
                // .then(updateFromResponse)
                // .catch(updateFromError)
                .then(resp => {
                    console.log(resp)
                    // saveJwtToken(resp.data.token)
                    return resp
                })
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