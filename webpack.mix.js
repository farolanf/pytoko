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

mix.js('toko/assets/js/app.js', 'static/toko/js')
  .sass('toko/assets/css/app.scss', 'static/toko/css')
  .disableNotifications();