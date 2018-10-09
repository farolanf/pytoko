
/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries. It is a great starting point when
 * building robust, powerful web applications using Vue and Laravel.
 */

import './bootstrap'
import './directives'

import Vue from 'vue'
import router from './router'
import store from './store'
import { loginWithJwt } from './helpers/account';

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

// import all components

const importAll = r => r.keys().forEach(key => {
    const name = key
        .replace(/.*\/(.+)\.vue$/, '$1')
        .replace(/(\w)([A-Z])/g, '$1-$2')
        .toLowerCase()
    Vue.component(name, r(key))
})

importAll(require.context('./components', true, /\.vue$/))

const app = new Vue({
    el: '#app',
    router,
    store,
    created () {
        loginWithJwt()
    }
});
