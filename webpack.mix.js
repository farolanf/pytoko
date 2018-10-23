const mix = require('laravel-mix');
const webpack = require('webpack')
const fs = require('fs')
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

const jsDir = 'toko/assets/components/js'
const cssDir = 'toko/assets/components/css'

fs.readdirSync(jsDir).forEach(file => {
  mix.js(path.resolve(jsDir, file), 'toko/static/toko/js')
})

fs.readdirSync(cssDir).forEach(file => {
  mix.sass(path.resolve(cssDir, file), 'toko/static/toko/css')
})

mix.js('toko/assets/js/app.js', 'toko/static/toko/js')
  .sass('toko/assets/css/app.scss', 'toko/static/toko/css')

mix.disableNotifications();