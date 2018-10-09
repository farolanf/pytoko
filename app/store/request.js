import store from '#/store'

export default {
    namespaced: true,
    state: {
        message: '',
        errors: {},
        error: false,
        status: null,
    },
    getters: {
        hasError: state => name => state.errors.hasOwnProperty(name),
        getError: state => (name, all = false) => {
            if (state.errors.hasOwnProperty(name)) {
                return all ? state.errors[name] : state.errors[name][0]
            }
            return all ? [] : ''
        }
    },
    mutations: {
        setError (state, { message = '', errors = {}, status = 200 } = {}) {
            state.message = message
            state.errors = errors
            state.status = status
            state.error = status >= 300
        },
        resetRequestState (state) {
            state.message = ''
            state.errors = {}
            state.status = null
            state.error = false
        }
    }
}

export function updateFromResponse (response) {
    let message = ''
    let errors = {}
    const error = response.status < 200 || response.status >= 300
    if (error) {
        errors = response.data
    } else if (response.data.message) {
        message = response.data.message
    }
    store.commit('request/setError', {
        message,
        errors,
        status: response.status
    })
    return response
}
export function updateFromError (err) {
    updateFromResponse(err.response)
    throw err
}