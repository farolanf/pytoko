import Vue from 'vue'
import { money } from '#/utils/data'

Vue.mixin({
    created () {
        this.money = money
    }
})