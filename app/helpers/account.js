import store from '#/store'

export function loginWithJwt () {
    if (!loadToken()) return
    store.dispatch('account/getUser')
        .catch(() => {
            removeToken()
        })
}

export function removeToken() {
    localStorage.removeItem('jwt')
}

export function saveToken (token) {
    localStorage.setItem('jwt', token)
}

export function loadToken () {
    return localStorage.getItem('jwt')
}