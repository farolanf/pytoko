import Vue from 'vue'
import store from '#/store'

Vue.directive('error', {
    update: setError,
    componentUpdated: setError,
})

function setError (el, binding) {
    const name = el.name || binding.arg
    const hasError = store.getters['request/hasError'](name)
    el.classList.toggle('is-danger', hasError)
}
