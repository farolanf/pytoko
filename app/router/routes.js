
const meta = {
    auth: true
}

const proxy = {
    template: '<router-view></router-view>'
}

const routes = [
    {
        path: '/', component: c('layout/AppLayout'),
        children: [
            { path: '', component: c('page/FrontPage'), name: 'front' },

            { path: 'tentang-kami', component: c('page/AboutPage'), name: 'about' },

            { path: 'masuk', component: c('user/page/LoginPage'), name: 'login' },

            { path: 'daftar', component: c('user/page/RegisterPage'), name: 'daftar' },

            { path: 'lupa-password', component: c('user/page/ForgotPasswordPage'), name: 'forgot-password' },
            
            { path: 'akun', component: c('user/page/Dashboard'), name: 'dashboard', meta },

            { path: 'akun/iklan-saya', component: c('page/MyAds'), name: 'my-ads', meta },

            { path: 'iklan/:id', component: c('page/EditAd'), name: 'edit-ad', meta },

            { path: 'pasang-iklan', component: c('page/PostAd'), name: 'post-ad', meta },

            { path: 'status', component: c('page/RequestStatusPage'), name: 'request-status' },

            { path: '*', component: c('NotFound') }
        ],
    },
]

function c(name) {
    return require(`@/${name}.vue`)
}

export default routes