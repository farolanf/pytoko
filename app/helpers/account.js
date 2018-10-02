import axios from 'axios'
import jwtDecode from 'jwt-decode'
import store from '#/store'

export function loginWithJwt () {
    const token = loadJwtToken()
    if (token) {
        verifyJwtToken(token).then(() => {
            store.dispatch('account/getUser')
        }).catch(() => {
            removeJwtToken()
        })
    }
}

export function getJwtPayload () {
    const token = loadJwtToken()
    if (!token) return
    return jwtDecode(token)
}

export function refreshJwtToken () {
    const token = loadJwtToken()
    if (!token) return

    const payload = jwtDecode(token)
    if (!payload) return

    if (payload.exp - Date.now()/1000 > 60*15) return
    
    axios.post('/api-token-refresh/', { token }, {
        refreshTokenRequest: true
    }).then(resp => {
        saveJwtToken(resp.data.token)
    })
}

export function verifyJwtToken (token) {
    return axios.post('/api-token-refresh/', { token })
}

export function removeJwtToken() {
    localStorage.removeItem('jwtToken')
}

export function saveJwtToken (token) {
    if (!token) throw new Error('saving invalid token')
    localStorage.setItem('jwtToken', token)
}

export function loadJwtToken () {
    return localStorage.getItem('jwtToken')
}