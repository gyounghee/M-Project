<template>
  <!-- @submit = v-on:submit -->
  <!-- prevent: 새로고침 방지 -->
 	<form @submit.prevent="signUp">
		<div id='signup'>
		<div class="form-inputs">
			<div>
				<label for="username">아이디</label>      
				<input id="username" type="text" 
				v-model="user.userid" placeholder="아이디" />
				<div v-if="!idValid">
					유효하지 않은 아이디입니다.			
				</div>
			</div>
			<div>
				<label for="password">비밀번호</label>
				<input id="password" type="password" @blur='passwordValid'
				v-model="user.password" placeholder="비밀번호"/>
				<div v-if="!passwordValidFlag">
					비밀번호는 숫자+영문자 조합으로 구성해주세요.
				</div>
			</div>
			<div>
				<label for="passwordcheck">비밀번호 확인</label>
				<input id="passwordcheck" type="password" @blur='passwordCheckValid' 
				v-model="passwordCheck" placeholder="비밀번호 확인"/>
				<div v-if="!passwordCheckFlag">
					비밀번호가 동일하지 않습니다.
				</div>
			</div>
		</div>
		</div>
		<button type='submit' class="btn">회원 가입</button>
		<div>
			<router-link tag='button' class='btn-signup' id='btn-signup' to="./">취소</router-link>
		</div>		
  	</form>
</template>
 
<script> 
	export default {
		data() {
    		return {
      	// form
			user:{
      			userid: null,
      			password: '',
			},
			passwordValidFlag: true,
      		passwordCheck: '',
      		passwordCheckFlag: true,
      		idValidflag : true,
  			};
		},
		computed: {
			idValid() {
				return /^[A-Za-z0-9]+$/.test(this.user.userid)
			}
		},
  		methods: {
			passwordValid () {
				// if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,16}$/.test(this.password)) {
				if (/^(?=.*[a-z])(?=.*[0-9]).{4,16}$/.test(this.user.password)) { 
				this.passwordValidFlag = true
				} 
				else { 
					this.passwordValidFlag = false 
				} 
			},
			passwordCheckValid() {
				if (this.user.password == this.passwordCheck) {
					this.passwordCheckFlag = true
				} else {
					this.passwordCheckFlag = false
				}
			},    	
			signUp() {
				if (this.user.userid == null || this.user.password == null || this.passwordCheck == null){
					alert('값을 입력해 주세요')
					return
				}
				if (!this.idValid || !this.passwordValidFlag || !this.passwordCheckFlag) {
					alert('유효성을 확인해 주세요')
					return
				} else {
				this.$http.post('http://35.76.37.170:8980/dogobesitytest/signup/',{
				user: this.user,
				})
				.then((res) => {
				if (res.status == 201) {					
					alert('회원가입 성공!');
					this.$router.replace({ name: "Login" });
				}
				if (res.status == 409) {
					alert('이미 존재하는 아이디 입니다');
				}
				})
				.catch((err) => {					
                    if(err.response.status == 409) {
						alert('이미 존재하는 아이디 입니다');
					} else {
						alert(err)
					}
				})
				}	
			},			
		}
  	}
</script>

<style>
    input {
    width:200px; 
    height:30px; 
	font-family: 'SDSamliphopangche_Basic';
    border-radius:5px;
	margin-bottom:20px;
}

	#signup .form-inputs {
		font-family: 'SDSamliphopangche_Basic';
		font-size: 20px; 
	}

	label[for='username']{
		margin-right:62px;
	}
	label[for='password']{
		margin-right:46px;
	}
	label[for='passwordcheck']{
		margin-right:10px;
	}
</style>