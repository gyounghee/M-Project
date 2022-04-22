import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {fas} from '@fortawesome/free-solid-svg-icons'
import axios from 'axios'
import VueLoading from 'vue-loading-template'

Vue.prototype.$http = axios;
Vue.config.productionTip = false
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(VueLoading,)

new Vue({
  router,
  render: function (h) { return h(App) },  
}).$mount('#app')

library.add(
  fas,
)
