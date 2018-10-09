import Vue from 'vue'
import store from '#/store'

Vue.directive('error', {
    update (el, binding) {
        const hasError = store.getters['request/hasError'](el.name || binding.value)
        el.classList.toggle('is-danger', hasError)
    }
})