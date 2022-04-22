<template>
  <div id='dogcheck'>
    <h1>견종선택</h1> 
    <div class="flex1">
      <div class="dac">       
        <img alt="Dog" src="../assets/da1.png" height="150px" width="150px">        
        <div>
          <label for="dac">
            <input type="checkbox" id="dac" value="Dachshund" v-model="checked" v-on:click= "check_one()">
            닥스훈트
          </label>
        </div>
      </div>        
      <div class="bea">
        <img alt="Dog" src="../assets/bea1.png" height="150px" width="150px">
        <div>
          <label for="bea">
            <input type="checkbox" id="bea" value="Beagle" v-model="checked" v-on:click= "check_one()">
            비글
          </label>
        </div>
      </div>
      <div class="ret">
        <img alt="Dog" src="../assets/ret1.png" height="150px" width="150px">        
        <div>
          <label for="ret">
            <input type="checkbox" id="ret" value="Retriever" v-model="checked" v-on:click= "check_one()">
            리트리버
          </label>
        </div>
      </div>
    </div>
    <div class="flex2">  
      <div class="mal">
        <img alt="Dog" src="../assets/mal1.png" height="150px" width="150px">        
        <div>
          <label for="mal">
            <input type="checkbox" id="mal" value="Maltese" v-model="checked" v-on:click= "check_one()">
            말티즈
          </label>
        </div>
      </div>   
      <div class="wel">
        <img alt="Dog" src="../assets/wel1.png" height="150px" width="150px">        
        <div>
          <label for="welsh">
            <input type="checkbox" id="welsh" value="Welsh Corgi" v-model="checked" v-on:click= "check_one()">
            웰시코기
          </label>
        </div>
      </div>
      <div class="chi">
        <img alt="Dog" src="../assets/chi1.png" height="150px" width="150px">        
        <div>
          <label for="chi">
            <input type="checkbox" id="chi" value="Chihuahua" v-model="checked" v-on:click= "check_one()">
            치와와
          </label>
        </div>
      </div>
    </div>
    <div>
      <br><br><span>선택한 견종: {{checked[0]}}</span><br>
      <button class="btn" @click="secure()">다음</button>
    </div>
  </div>
</template>
<script>
export default {
    name:'dogcheck',
    data(){
        return{
            checked: [],
        }
    },
    mounted() {
      this.$emit("authenticated", JSON.parse(localStorage.getItem('authenticated')) );
      if(!this.$parent.authenticated) {
        this.$router.replace({ name: "Login" });
      }
    },
    methods: {
      check_one:function(){
        this.checked = [];
      },

      secure(){
        localStorage.setItem('dog_breed',JSON.stringify(this.checked[0]));        
        this.$router.push("./dogimage").catch(()=>{});    
      },
    }
}
</script>

<style scoped>
@font-face {
    font-family: 'SDSamliphopangche_Basic';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts-20-12@1.0/SDSamliphopangche_Basic.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

h1 {
  margin-bottom:50px;
}
input{
  width:20px;
  height:20px;
  margin-bottom:30px;
}
label{
  font-family: 'SDSamliphopangche_Basic';
  font-size:30px;
}
.btn{
  margin-top:50px;
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