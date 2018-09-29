import jwtDecode from 'jwt-decode'
import store from '#/store'

export function loginWithJwt () {
    if (!loadJwtToken()) return
    store.dispatch('account/getUser')
        .catch(() => {
            removeJwtToken()
        })
}

export function refreshJwtToken () {
    const token = loadJwtToken()
    if (!token) return

    const decoded = jwtDecode(token)
    console.log(decoded)
    if (decoded.exp - Date.now() > 60*15) return

    axios.post('/api-token-refresh', { token }).then(resp => {
        saveJwtToken(resp.data.token)
    })
}

export function removeJwtToken() {
    localStorage.removeItem('jwtToken')
}

export function saveJwtToken (token) {
    localStorage.setItem('jwtToken', token)
}

export function loadJwtToken () {
    return localStorage.getItem('jwtToken')
}