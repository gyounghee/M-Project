import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter);

export default new VueRouter({
	mode:'history', //해쉬값 제거 방식
    routes: [
      {
        path: '*',
        component: () => import('../components/NotFoundComponent.vue'),
      }, 
      {
        path: '/', 
        redirect: '/dogobesitytest' 
    }, {
        path: '/dogobesitytest',
        name: 'Login',
        component: () => import('../views/Login.vue'),
    }, {
      path: '/dogobesitytest/checkbox',
      name: 'Check',
      component: () => import('../views/Checkbox.vue'),
    }, {
      path: '/dogobesitytest/signup',
      name: 'SignUp',
      component: () => import('../views/SignUp.vue'),
    }, {
      path: '/dogobesitytest/dogimage',
      name: 'Secure',
      component: () => import('../views/Secure.vue'),
    }, {
      path: '/dogobesitytest/testresult',
      name: 'Result',
      component: () => import('../views/Result.vue'),
    }]
});


