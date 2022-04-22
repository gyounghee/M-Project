<template>
  <div id = "secure">
    <h1>사진첨부</h1>
    <br><br><span>선택한 견종: {{checked}}</span><br>
  <div class="container">
    <div class="file-upload-container" 
      @dragenter="onDragenter"
      @dragover="onDragover"
      @dragleave="onDragleave"
      @drop="onDrop"
      @click="onClick"
    >
      <div class="file-upload">
        Drag & Drop Files
      </div>
    </div>
    <!-- 파일 업로드 -->
    <input type="file" ref="fileInput" class="file-upload-input" @change="onFileChange" multiple>
    <!-- 업로드된 리스트 -->
    <div class="file-upload-list">
      <div class="file-upload-list__item" v-for="(file, index) in fileList" :key="index">
        <div class="file-upload-list__item__data">
          <img id='img1' class="file-upload-list__item__data-thumbnail" :src="file.src">
          <div class="file-upload-list__item__data-name">
            {{ file.name }}
          </div>
        </div>
        <div class="file-upload-list__item__btn-remove" @click="handleRemove(index)">
          삭제
        </div>
      </div>
    </div>
  </div>
    
    
    
    <button class="btn" @click="result">결과</button>
    
    <MyModal @click="closeModal" v-if="modal">
      <!-- default 슬롯 콘텐츠 -->      
      <h1>비만 여부를 판별 중입니다!</h1>
      <div class="spinner-container">
        <div class="spinner" />     
      </div>      
      <!-- /default -->
      <!-- footer 슬롯 콘텐츠 -->
      <template slot="footer">
          <button @click="doSend">취소</button>
      </template>
    </MyModal>
  </div>

</template>

<script>
import MyModal from '../components/MyModal.vue'
export default {
  components: {MyModal},
  name: 'Secure',
  data() {
      return {
        fileList : [],
        isDragged : '',
        upload: { userid:JSON.parse(localStorage.getItem('userid')) ,image:null ,dog_breed:JSON.parse(localStorage.getItem('dog_breed')) },
        modal: false,
        checked: JSON.parse(localStorage.getItem('dog_breed')),    
    }
  },
  mounted() {
    this.$emit("authenticated", JSON.parse(localStorage.getItem('authenticated')) );
    if(!this.$parent.authenticated) {
        this.$router.replace({ name: "Login" });
    }
  },  
  methods: {    
    result(){    
      var img1 = document.getElementById('img1').src;           
      localStorage.setItem('image', JSON.stringify(img1));
      var img2 = JSON.parse(localStorage.getItem('image'));
      this.upload.image = img2.split('base64,')[1]     
      // alert(JSON.stringify(this.upload));
      if ( this.upload.userid == null || this.upload.image == null || this.upload.dog_breed == null){
					alert('이미지를 업로드 해 주세요')
					return
      } else {
        this.modal = true;
        this.$http.post('http://35.76.37.170:8980/dogobesitytest/dogimage/',{
				upload: this.upload,
				})        
				.then((res) => {
				if (res.status == 201) {          
          this.result = res.data['text'];
          let accuracy = res.data['accuracy'];
          let img_name = res.data['image'];
          localStorage.setItem('image_name', JSON.stringify(img_name));
          localStorage.setItem('result', JSON.stringify(this.result));
          localStorage.setItem('accuracy', JSON.stringify(accuracy));
          this.modal = false;
          this.$router.push("./testresult");
				}
				if (res.status == 400) {
					alert(res.data.message);
          this.$router.push("./dogimage");
				} 
        if (res.status == 204) {          
          alert('강아지 사진을 넣어주세요');
          this.modal = false;
	      }
				})
				.catch(function (error) {
				alert('error');
				})
				};      
    },
    closeModal() {
      this.modal = false
    },
    doSend() {      
      this.closeModal();
      this.$router.push("./dogimage").catch(()=>{});    
    },
    onClick () {
        this.$refs.fileInput.click()
    },
    onDragenter (event) {
        // class 넣기
      this.isDragged = true
    },
    onDragleave (event) {
        // class 삭제
      this.isDragged = false
    },
    onDragover (event) {
        // 드롭을 허용하도록 prevetDefault() 호출
      event.preventDefault()
    },
    onDrop (event) {
        // 기본 액션을 막음 (링크 열기같은 것들)
      event.preventDefault()
      this.isDragged = false
      const files = event.dataTransfer.files
      this.addFiles(files)
    },
    onFileChange (event) {
        const files = event.target.files
      this.addFiles(files)
    },
    async addFiles (files) {
        for(let i = 0; i < files.length; i++) {
          const src = await this.readFiles(files[i])
        files[i].src = src
        this.fileList.push(files[i])
      }
    },

    // FileReader를 통해 파일을 읽어 thumbnail 영역의 src 값으로 셋팅
    async readFiles (files) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader()
        reader.onload = async (e) => {
            resolve(e.target.result) 
        }
        reader.readAsDataURL(files)
      })
    },
    handleRemove (index) {
        this.fileList.splice(index, 1)
    }
  }
}
  
</script>

<style lang="scss">
.select {
  margin-top:30px;
}

.container {
  display: block;
  min-height: 300px;
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
  margin-top:50px;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 240px;
}
.spinner {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 10px solid #e0e0e0;
  border-bottom: 10px solid #fe9616;
  animation: spin 0.7s linear infinite;
  position: relative;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.file-upload {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  border: transparent;
  border-radius: 20px;
  cursor: pointer;
  &.dragged {
    border: 1px dashed powderblue;
    opacity: .6;
  }
  &-container {
    display: flex;
    height: 300px;
    padding: 20px;
    margin: 0 auto;
    box-shadow: 0 0.625rem 1.25rem #0000001a;
    border-radius: 20px;
  }
  &-input {
    display: none;
  }
  &-list {
    margin-top: 10px;
    width: 100%;
    &__item {
      padding: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      &__data {
        display: flex;
        align-items: center;
        &-thumbnail {
          margin-right: 10px;
          border-radius: 20px;
          width: 120px;
          height: 120px;
        }
      }
      &__btn-remove {
        cursor: pointer;
        border: 1px solid powderblue;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 5px;
        border-radius: 6px;
      }
    }
  }
}
</style>