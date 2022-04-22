<template>
  <div id="app">
    <div id="header">
      <main-header/>
    </div>
    <div id="nav">
      <router-link v-if="authenticated" to="/dogobesitytest/checkbox">견종선택</router-link>
      <router-link v-if="authenticated" to="/dogobesitytest/dogimage">검사</router-link>
      <router-link v-if="authenticated" to="/dogobesitytest/testresult">결과</router-link>
      <router-link v-if="authenticated" to="/dogobesitytest" v-on:click.native="logout()" replace>Logout</router-link>
    </div>
    <router-view @authenticated="setAuthenticated"/>
    <div id="footer">
      <main-footer/>
    </div>
  </div>
</template>

<script>
import MainHeader from './components/MainHeader.vue'
import MainFooter from './components/MainFooter.vue'
    export default {
        name: 'App',
        components: {
          'main-header':MainHeader,
          'main-footer':MainFooter
        },
        data() {
            return {
                authenticated: false,                
            }
        },
        methods: {
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                this.authenticated = false;
                localStorage.clear();
            }
        }
    }
</script>

<style lang="scss">

@font-face {
    font-family: 'SDSamliphopangche_Outline';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts-20-12@1.0/SDSamliphopangche_Outline.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

#app {
  text-align: center;
  font-size: 20px; 
  font-family: 'SDSamliphopangche_Outline';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
}

#nav {
  padding: 30px;
}

#nav a {
  font-size: 25px; 
  color: black;
  padding-right: 10px;
}

#nav a:not(:first-child) {
  font-size: 25px;
  border-left: 1px solid black;
  padding-left: 10px; 
}

#nav a.router-link-exact-active {
  color: orange;
}

.flex1{
  display:flex;
  width:100%;
  height:100%;
  flex-direction: row;
  flex-wrap:wrap;
  justify-content: center;
  align-items: center;
}
.flex2{
  display:flex;
  width:100%;
  height:100%;
  flex-direction: row;
  flex-wrap:wrap;
  justify-content: center;
  align-items: center;
}
.dac{
  flex:3;  
}
.bea{
  flex:3;
}
.mal{
  flex:3;
}
.ret{
  flex:3;
}
.wel{
  flex:3;
}
.chi{
  flex:3;
}
</style>
