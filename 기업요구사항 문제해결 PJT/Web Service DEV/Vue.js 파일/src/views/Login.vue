<template>
    <div id="login">
        <img alt="Dog" src="../assets/Dog.jpg" height="350px" width="350px" id="login_img">
        <h2>로그인</h2>
        <div class="form-inputs">
            <label for="username">아 이 디</label>
            <input type="text" id="username" name="username"  
            v-model="user.userid" placeholder="Username" />
        </div>
        <div class="form-inputs">
            <label for="password">비밀번호 </label>
            <input type="password" id="password" name="password" 
            v-model="user.password" placeholder="Password" />
        </div>
        <button class="btn" @click="login">Login</button>
        <button class="btn" @click="signup">회원가입</button>        
    </div>
</template>

<script>    
    export default {        
        name: 'Login',
        data() {
            return {
                user: {
                    userid: "",
                    password: ""
                },    
                // JSON.parse(localStorage.getItem('userData')) || '',                
            }
        },
        mounted() {
            localStorage.clear();
        },
        methods: {
            login() {                                
                this.$http.post('http://35.76.37.170:8980/dogobesitytest/', {
                        user: this.user,
                    })
                .then(
                    (res) => {
                        if (res.status == 200 ) {                                                                       
                            localStorage.setItem('userid',JSON.stringify(this.user.userid));
                            localStorage.setItem('authenticated',JSON.stringify("true"));                           
                            this.$emit("authenticated", true);
                            this.$router.replace({ name: "Check" });
                        } else {
                            alert(res.data.message);                                    
                        }
                    
                    },
                    (err) => {
                        alert('로그인 실패! 아이디와 비밀번호를 확인해주세요')
                    }
                )
                .catch((err) => {
                    alert(err);
                });  
            },
            signup(){
                this.$router.push("../dogobesitytest/signup").catch(()=>{});
            },            
        
        }
    }
</script>

<style lang="scss">

@font-face {
    font-family: 'SDSamliphopangche_Basic';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts-20-12@1.0/SDSamliphopangche_Basic.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

h2{ margin-top:30px; margin-bottom:30px;}

input {
    width:200px; 
    height:30px; 
    border-radius:5px;}

#login .form-inputs {
    padding-bottom: 20px;
    font-family: 'SDSamliphopangche_Basic';
    font-size: 20px;}
#login_img{    
    height: 350px;
    width: 100%;
    max-width: 350px;     
    display: center;
    justify-content: center;
    align-items: center;
}

label[for='username']{
    margin-right:20px;
}
label[for='password']{
    margin-right:9px;
}

.btn{
    margin-top:30px;
    height: 70px;
    width: 180px;
    font-size: 40px;
    border: 3px solid black;
    border-radius:20px;
    background-color: white;
    color: black; padding: 5px;
    font-family: 'SDSamliphopangche_Outline';
    -webkit-transition-duration: 0.4s; 
    transition-duration: 0.4s;
}
 
.btn-signup{
    margin-top:30px;
    height: 40px;
    width: 100px;
    font-size: 20px;
    border: 2px solid black;
    border-radius:10px;
    background-color: white;
    color: black; padding: 5px;
    font-family: 'SDSamliphopangche_Outline';
    -webkit-transition-duration: 0.4s; 
    transition-duration: 0.4s;
}

.btn:hover {
    background: pink;
    color: black;
}
.btn-signup:hover {
    background: pink;
    color: black;
}
button{
    margin-left:10px;
}
</style>