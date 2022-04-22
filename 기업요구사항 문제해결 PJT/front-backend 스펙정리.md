**추가 사항이나 수정 사항이 생기면 바로 말씀해주세요**

**모든 Text 데이터는 JSON 형태로 받으며, File과 함께 데이터를 주고 받는 경우는 multipart/form-data로**

**변경 사항 → 이미지도 json 형태로 하기로 바꿈**
-
-
**초기 페이지**
< http://35.76.37.170:80/dogobesitytest >
	* POST 요청 (로그인 시도) 
	- 주고 받는 데이터 
		- {user: {userid: "test11", password: "a111"}}
	- 성공 
		- 견종 선택 페이지로 < http://35.76.37.170:80/dogobesitytest/dogimg >
		- status 200  
	- 실패 시 
		- 다시 초기 페이지로 < http://35.76.37.170:80/dogobesitytest >
		- status 400
-
-

**회원가입 페이지**
< http://35.76.37.170:80/dogobesitytest/signup >
	* POST 요청
	- 주고 받는 데이터 
		- {user: {userid: "test11", password: "a111"}}
		- 존재하는 id일 경우
			- status 409
			- status 201
		- 존재하지 않는 id일 경우
			- 유효성 검증 성공 시
				- id와 암호화 된 비밀번호를 DB에 저장
				- status 201
			- 유효성 검사 실패 시
				- status 400
-
-
**견종 선택( or 이미지 업로드 )페이지**
< http://35.76.37.170:80/dogobesitytest/dogimage >
	* POST 요청
	- 주고 받는 데이터 ( multipart/form-data 형식으로 )   →   JSON형태로 주고 받는 것으로 변경됨 
		- {upload :{ userid: "ex", image:"base64형식", dog_breed:"견종"}}
- userid와 dog_breed 같은 데이터의 경우 프론트엔드에서 저장해뒀다가 사용자가 이미지 업로드 후 결과버튼을 누를 시 함께 서버에 전송되도록 구현
		- 성공시
			- userid, image, dog_breed 데이터가 들어오면 서버에서 처리 후 "정상입니다" 혹은 "비정상입니다" 라는 텍스트를 JSON 형태로 리턴
			- status 200
		- 실패 시
			- 이미지 업로드 페이지로  < http://35.76.37.170:80/dogobesitytest/dogimage >
			- status 400
-
-
**결과페이지**
< http://35.76.37.170:80/dogobesitytest/testresult >
	* PUT 요청
	- 주고 받는 데이터 
		- {imgae : "이미지명"}
		- Testresult DB에 해당 이미지가 있으면
			- 해당 row의 like column값 1로 변경 후 
			- 웹에 총 테스트 수와 like값이 1인 테스트 수를 json 형태로 보냄
			- status 200
		- Testresult DB에 해당 이미지가 없으면
			- status 400












