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
        hasError: state => name => state.errors && state.errors.hasOwnProperty(name),
        getError: state => name => state.errors 
            ? Array.isArray(state.errors[name])
                ? state.errors[name][0]
                : state.errors[name]
            : ''
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
    store.commit('request/setError', {
        message: response.data.message || response.data.non_field_errors && response.data.non_field_errors[0],
        errors: response.data.errors || response.data.non_field_errors,
        status: response.status
    })
    return response
}
export function updateFromError (err) {
    updateFromResponse(err.response)
    throw err
}