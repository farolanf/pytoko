import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import store from '#/store'

Vue.use(VueRouter)

const router = new VueRouter({
    routes,
    mode: 'history',
    linkActiveClass: 'is-active'
})

router.beforeEach((to, from, next) => {
    
    // clear page errors when navigating away from a page
    store.commit('clearError')

    // clear request error when navigating away from a page except to the status page
    if (to.name !== 'request-status') {
        store.commit('request/resetRequestState')
    }
    
    next()
})

export default router