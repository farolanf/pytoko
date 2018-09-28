const mix = require('laravel-mix');
const webpack = require('webpack')
const path = require('path')

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix.webpackConfig({
  resolve: {
    alias: {
      '#': path.resolve(__dirname, 'app'),
      '@': path.resolve(__dirname, 'app/components')
    }
  },
  plugins: [
    new webpack.ProvidePlugin({
      mapState: ['vuex', 'mapState'],
      mapMutations: ['vuex', 'mapMutations'],
      mapGetters: ['vuex', 'mapGetters'],
      mapActions: ['vuex', 'mapActions'],
    })
  ]
})

mix.js('app/app.js', 'static/toko/js')
  .sass('app/css/app.scss', 'static/toko/css')
  .disableNotifications();

mix.copy('static/toko', 'toko/static/toko')

if (process.env.NODE_ENV === 'production') {
  mix.version();
}