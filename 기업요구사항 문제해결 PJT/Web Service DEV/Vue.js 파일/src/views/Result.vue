<template>
<div>
    <h1>결과</h1>
    <br><br><span>선택한 견종: {{checked}}</span><br>
    <div class="result_container">
      <img :src='img' class="result_img" />           
    </div>
    <h2 id='result_text'> {{ result }}</h2>
    <h3 id='result_text'> [비만일 확률 : {{accuracy}}%] </h3>
    <div class = "like">
      <span> <font-awesome-icon icon="fa-solid fa-heart" color=tomato font-size=35px class=fa-beat v-on:click="add()" /> 
       {{likecnt}} </span><br><br>
      <div v-if='count_show'>
        이용자 수 :{{count.total_count}} 좋아요 수 :{{count.like_count}}
      </div>
    </div>
    <div class="sns">
      공유하기<br><br>
      <img class="kakao_btn" src="@/assets/kakao.png" @click="kakaoLink" />
      <img class="twitter_btn" src="@/assets/twitter.png" @click="twitterLink"/>
      <img class="facebook_btn" src="@/assets/facebook.png" @click="facebookLink"/>
      <img class="link_btn" src="@/assets/link.png" @click="linkCopy"/>
    </div>
    <div class="diet"><br>
      반려견 체중 관리법<br>
      <a href ="https://petdoc.co.kr/ency/224" target='_blank' >
        <img class="diet" src="@/assets/diet.png" id="diet"/></a><br>
    </div>
    <div class="food">
      다이어트 사료 추천<br>
      <a href ="https://www.google.com/search?q=%EB%B0%98%EB%A0%A4%EA%B2%AC+%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8+%EC%82%AC%EB%A3%8C&ei=ht9LYv7qB4X7-QaN_qH4CQ&ved=0ahUKEwj-xdHbo_z2AhWFfd4KHQ1_CJ8Q4dUDCA4&uact=5&oq=%EB%B0%98%EB%A0%A4%EA%B2%AC+%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8+%EC%82%AC%EB%A3%8C&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEAcQHjoHCAAQRxCwAzoECAAQDToICAAQDRAFEB5KBAhBGABKBAhGGABQlwRY7wlg1wpoAnABeAGAAXGIAeQGkgEDMC44mAEAoAEByAEFwAEB&sclient=gws-wiz" target='_blank'>
        <img class="food" src="@/assets/food.png" target='_blank' id="food" /></a>
    </div>
</div>
</template>


<script>  
  export default {
    name: 'App',
    data() {
      return{
        img: JSON.parse(localStorage.getItem('image')),
        likecnt : "좋아요",
        count : {total_count:null, like_count:null},
        count_show : false,
        result: JSON.parse(localStorage.getItem('result')),
        checked: JSON.parse(localStorage.getItem('dog_breed')),
        accuracy: JSON.parse(localStorage.getItem('accuracy')),
      }
    },
    mounted() {
      this.$emit("authenticated", JSON.parse(localStorage.getItem('authenticated')) );
      if(!this.$parent.authenticated) {
        this.$router.replace({ name: "Login" });
      }
    },
    methods:{
      // getLike() {
      //     this.$http.get('http://35.76.37.170:8980/dogobesitytest/testresult/')
      //           .then(
      //               (res) => {
      //                   if (res.status == 200 ) {
      //                     like.total_count = res.data['total_count'];
      //                     like.like_count = res.data['like_count'];
      //                     count_show = true;
      //                   }                     
      //               },
      //               (err) => {
      //                   alert(res.data.message)
      //               }
      //           )
      //           .catch((err) => {
      //               alert(err);
      //           })
      // },    
      add(){
        if (this.likecnt == "좋아요") {         
          this.$http.put('http://35.76.37.170:8980/dogobesitytest/testresult/', {
                        image: JSON.parse(localStorage.getItem('image_name')),
                    })
                .then(
                    (res) => {
                        if (res.status == 200 ) {
                          this.likecnt = "감사합니다!"  
                          this.count.total_count = res.data['total_count'];
                          this.count.like_count = res.data['like_count'];
                          this.count_show = true;                        
                        } else {
                            alert(res.data.message);                                    
                        }
                    
                    },
                    (err) => {
                        alert(res.data.message)
                    }
                )
                .catch((err) => {
                    alert(err);
                })
        } else {
          alert('좋아요는 한번만 가능합니다!')
        }
      },
      kakaoLink () {
          window.Kakao.Link.sendDefault({
            objectType:'feed',
            content:{
              title:'강아지 정상/비만 판별기',
              description:'우리 강아지는 정상일까 비만일까',
              imageUrl:'http://35.76.37.170/img/Dog.9d7ce6f7.jpg',
              link:{
                mobileWebUrl:
                  'https://developers.kakao.com',
                webUrl:
                  'https://developers.kakao.com'
            }},
          buttons: [
            {
              title: '웹으로 보기',
              link: {
                mobileWebUrl: '카카오공유하기 시 클릭 후 이동 경로',
                webUrl: '카카오공유하기 시 클릭 후 이동 경로',
              },
            },
          ],
        })
        },
        twitterLink(){
          var sendText = "강아지 정상/비만 판별기"; 
          var sendUrl = "hhttp://35.76.37.170"; 
          window.open("https://twitter.com/intent/tweet?text=" + sendText + "&url=" + sendUrl);
        },
        facebookLink(){
          var sendUrl = "http://35.76.37.170"; 
          window.open("http://www.facebook.com/sharer/sharer.php?u=" + sendUrl);
        },
        linkCopy() {
          	var url = '';
	          var textarea = document.createElement("textarea");
	          document.body.appendChild(textarea);
	          url = window.document.location.href;
	          textarea.value = url;
	          textarea.select();
	          document.execCommand("copy");
	          document.body.removeChild(textarea);
	          alert("URL이 복사되었습니다.")
        },      
    }
  }
</script>

<style>
.result_img {
  margin-top:20px;
  height: 350px;
  width: 100%;
  max-width: 350px;  
  box-shadow: 0 0.625rem 1.25rem #0000001a;
  border-radius: 20px;
  display: center;
  justify-content: center;
  align-items: center;
}
.like{
  margin-top:50px;
  margin-bottom:40px;
  font-size:30px;
}
.button{
  margin-top:50px;
  margin-right : 10px;
  font-size: 20px;
  border: 3px solid black;
  border-radius:10px;
  color: black; padding: 5px;
  font-family: 'SDSamliphopangche_Outline';
  -webkit-transition-duration: 0.4s; 
  transition-duration: 0.4s;
}
.button:hover {
  background: orange;
  color: black;
}

.sns{
  padding-top:25px;
  text-align:center;
  font-size:30px;
}
.diet{
  font-size:30px;
  margin-top:20px;
  margin-bottom:100px;
  height:100px;
}
.food{
  font-size:30px;
  height:100px;
}
</style>