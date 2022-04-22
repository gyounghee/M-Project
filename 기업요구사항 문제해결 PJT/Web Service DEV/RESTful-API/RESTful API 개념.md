### 개념
    * REST (Representational State Transfer)   
        - 클라이언트 ↔ 서버의 통신방식   
        - URI와 HTTP를 이용한, 통신 목적의 아키텍처 스타일(유형)   
            +) URI(Uniform Resource Identifier)    
                : 문서, 그림, 영상 등의 자원 식별용 이름(경로)    
            +) 아키텍처 스타일 : 아키텍처(구조)의 종류(유형, 스타일, 타입)
                ex) 클라이언트/서버,  저장소,  파이프/필터,   REST
        - REST는 아키텍처 제작 시 사용되는 가이드 정도의 의미로 사용되며 명확히 준수해야할 표준은 없다

    * RESTful
        - REST가 적용된 시스템

    * REST API
        - REST가 적용된 API

    * RESTful
        - REST API를 제공하는 시스템


### REST의 6가지 조건
    * REST는 6가지 조건을 만족해야 함
        1. 일관된 인터페이스
            - URI 사용, HTTP 메소드 사용, RPC 미호출 등의 `지정된 인터페이스`를 준수
        2. 클라이언트/서버 (Client-Server)
            - 클라이언트는 서버에 `요청(request) 메세지`를 전송하고
            - 서버는 요청에 대한 `응답(response) 메세지`를 전송한다
        3. 비연결성(Statelessness)
            - 세션 등 `이전 상황(문맥)` 없이도 통신할 수 있다
        4. 캐시 가능 (Cacheable)
            - 서버의 응답 메세지는 `캐싱(저장 후 재사용)`될 수 있다.
        5. 계층화된 시스템 (Layered system)
            - 계층별로 기능이 분리된다.
            - 그러므로 중간 계층의 기능(로드 밸런싱, 서버증설, 인증 스스템 도입 등)이 변경되어도 통신에 영향을 주지 않는다.
        6. 주문형 코드(code on demand) (선택)
            - 손쉬운 데이터 처리를 위해 서버는 클라이언트에서 실행될 스크립트를 전송할 수 있다.


### REST API 만들기
    * API는 기본적인 CRUD를 위해 사용됨
    * API가 필요한 URL을 만들 때 
        - 표준을 만드는 것이 중요!!! (명확한 패턴)
        - URL에서는 동사를 사용하지 않는다. (명사만 사용)
        - 동사를 쓰는 대신에 HTTP methods를 사용하여 인터랙션 
            - HTTP methods : GET(읽기), POST(생성), PUT(업데이트), DELETE(삭제)
        - **`HTTP methods + 명사`** 방식을 사용 

### REST, REST API, RESTful의 개념, 설계 기본 규칙, 예시 등 
            - 참고자료 
                - https://gmlwjd9405.github.io/2018/09/21/rest-and-restful.html 
                - https://sanghaklee.tistory.com/57


### * restful api server 만들기 
    +) api server를 테스트 하기 위한 툴 설치 
        - 테스트 툴은 < insomnia > 활용 

    1. conda activate 가상환경
        - 가상환경 : p_youtube

    2. pip install --upgrade pip 

    3. pip install django

    4. django-admin startproject 프로젝트이름
        - 프로젝트 이름 : restfulapiserver

    5. Django REST framework 사용을 위한 설치   
        : 간단한 설정만으로 django를 restful api server로 만들어주는 프레임워크
        - pip install djangorestframework
        - pip install markdown
        - pip install django-filter

    6. settings.py에 source 추가  
        - 공식 홈페이지 참고 ( https://www.django-rest-framework.org/ )
        1. ALLOEWED_HOST에 (*) 추가
            ```
            ALLOWED_HOSTS = ['*']
            ```
        2. INSTALLED_APPS에 'rest_framework' 추가    
            ```
            INSTALLED_APPS += [
                'rest_framework'
            ]
            ```
        3. REST_FRAMEWORK 추가  
            ```
            REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
                ]
            }
            ```
        - Django는 앱 단위로 관리하기 때문에 방금 설치한 rest_framework 앱을 명시해 주어야 하며, rest_framework에 권한 설정을 하기 위한 설정도 넣어줌

    7. 프로젝트폴더 > urls.py 에 코드 추가    
        ```
        from django.urls import path, include

        urlpatterns = [
        ...
        path('api-auth/', include('rest_framework.urls')),
        ]
        ```

    8. superuser 생성
        -  manage.py createsuperuser
            - 생성한 id, pw, email
            - id : superuser /  pw : 0000  / email : superuser@naver.com 

    9.  manage.py startapp 앱이름 
        - 앱 이름 : addresses

    10. 앱폴더 > models.py에 모델 생성
        ```
        class Addresses(models.Model):
        name = models.CharField(max_length=10)
        address = models.TextField()
        created = models.DateTimeField(auto_now_add=True)
            class Meta:
                # 조회 시 created를 기준으로 내림차순으로 표시됨 (순서대로 표시하기 위함)
                ordering = ['created']
        ```

    11. migration하기 
        -  manage.py makemigrations 앱이름
        -  manage.py migrate

    12. 앱폴더 > serializers.py 파일 생성 후 코드 추가   
        ```
        from rest_framework import serializers
        from .models import Addresses    

        class AddressesSerializer(serializers.ModelSerializer):
            class Meta:
                model = Addresses
                fields = ['name','address','created']
        ```

    13. 앱 폴더 > views.py   
        ```
        from django.shortcuts import render
        from django.http import HttpResponse, JsonResponse
        from django.views.decorators.csrf import csrf_exempt
        from rest_framework.parsers import JSONParser

        from .models import Addresses
        from .serializers import AddressesSerializer

        ## 모든 건수 조회하는 코드
        @csrf_exempt
        def address_list( request ) :
            # GET요청이 들어오면 전체 address list를 내려주는  
            if request.method == 'GET':
                query_set = Addresses.objects.all()
                serializer = AddressesSerializer(query_set, many=True)  
                return JsonResponse(serializer.data, safe=False)
            
            # POST 요청이 들어오면 만들어주도록 
            elif request.method == 'POST':
                data = JSONParser().parse(request)
                serializer = AddressesSerializer(data=data)
                if serializer.is_valid() :    
                    serializer.save()   
                    return JsonResponse(serializer.data, status=201)  
                return JsonResponse(serializer.errors, status=400)  
        ```

    14. 프로젝트폴더 > urls.py 에 코드 추가    
        ```
        from django.contrib import admin
        from django.urls import path, include
        from addresses import views  

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api-auth/', include('rest_framework.urls')),
            path('addresses/', views.address_list),
    ]
        ```

    15. (선택) 시간 설정을 한국시간으로 설정
        - 프로젝트 폴터 > settings.py
        ```
        # 변경해줘야할 코드
        TIME_ZONE = 'Asia/Seoul'
        USE_TZ = False
        ```


    # **TEST** - `insomnia`
        - `Ctrl+N`을 하여 request생성
            1. GET http://127.0.0.1:8000/addresses/
                - 저장된 데이터들이 JSON형태로 보이면 성공
            
            2. POST http://127.0.0.1:8000/addresses/
                - JSON 형태로 데이터를 보내줘야함 
                ```
                {
                    "name" : "경이",
                    "address" : "집"
                }
                ```

                - 결과가 이렇게 나온다면 성공 
                ```
                    {
                        "name": "경이",
                        "address": "집",
                        "created": "2022-03-22T10:08:45.107967Z"
                    }
                ```

    **위에서 했던 것이 다수의 건수를 조회하는 코드였다면 이번에는 단건 조회에 대해 살펴보자.**

    16. 앱 폴더 > views.py
        - 단건 조회 코드 추가  
        ```
        @csrf_exempt
        def address( request, pk ) :   # 단건 조회
            select_adr = Addresses.objects.get(pk=pk)

            if request.method == 'GET':
                serializer = AddressesSerializer(select_adr)  
                return JsonResponse(serializer.data, safe=False)
            
            elif request.method == 'PUT' :
                data = JSONParser().parse(request)
                serializer = AddressesSerializer(select_adr, data=data)
                if serializer.is_valid() :    
                    serializer.save()  
                    return JsonResponse(serializer.data, status=201) 
                return JsonResponse(serializer.errors, status=400)

            elif request.method == 'DELETE' :
                select_adr.delete()  
                return HttpResponse(status=204) 
        ```

    17. 프로젝트 폴더 > urls.py
        - urlpatterns = [] 에 코드 추가
        ```
        path('addresses/<int:pk>', views.address),
        ```


    **이번엔 DB에 저장된 PW가 사용자가 입력한 PW가 맞는지 확인 후 응답보내기**

    18. 앱 폴더 > views.py
        - 코드 추가
        ```
        @csrf_exempt
        def login(request) :
            if request.method == 'POST':
                data = JSONParser().parse(request)
                search_name = data['name']
                select_adr = Addresses.objects.get(name=search_name)
                # print(data['address'])     #  읽어온 비밀번호
                # print(select_adr.address)  #  저장된 비밀번호 
                if data['address'] == select_adr.address :
                    return HttpResponse(status=200)
                else :
                    return HttpResponse(status=400)
        ```

    19. 프로젝트 폴더 > urls.py
        - urlpatterns =[] 에 코드 추가
        ```
        path('login/', views.login),
        ```





### vue.js와 django 연동하여 CRUD REST 실습
1. conda activate 가상환경
    - 가상환경 : practice

2. pip install --upgrade pip 

3. pip install django

4. django-admin startproject 프로젝트이름
    - 프로젝트 이름 : dogtest

5. python manage.py startapp 앱이름
    - 앱 이름 : dogtest_app

6. Django REST framework 사용을 위한 설치   
    - pip install djangorestframework

7. settings.py에 source 추가  
    - 공식 홈페이지 참고 ( https://www.django-rest-framework.org/ )
    1. ALLOEWED_HOST에 (*) 추가
        ```
        ALLOWED_HOSTS = ['*']
        ```
    2. INSTALLED_APPS에 'rest_framework' 추가    
        ```
        INSTALLED_APPS += [
            'rest_framework'
        ]
        ```
    3. REST_FRAMEWORK 추가  
        ```
        REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
            ]
        }
        ```

8. 모델 생성 & migration
    1. 모델 생성
        - 프로젝트 폴더 > models.py
        ```
        from django.db import models

        # Create your models here.
        class Serviceuser(models.Model):
            user_id = models.CharField(max_length=15, primary_key=True)
            user_pw = models.CharField(max_length=20)
            created = models.DateTimeField(auto_now_add=True)
            class Meta:
                ordering = ['created']
        ```
    2. migration
        - python manage.py makemigrations 
        - python manage.py migrate 

9. 앱 폴더 > serializers.py 생성
    ```
    from rest_framework import serializers
    from .models import Serviceuser

    class ServiceuserSerializer(serializers.ModelSerializer):
        class Meta:
            model = Serviceuser
            fields = '__all__'
    ```

10. 앱 폴더 > viewsets.py  생성
    ```
    from rest_framework import viewsets
    from .models import Serviceuser
    from .serializers import ServiceuserSerializer

    class ServiceuserViewSet(viewsets.ModelViewSet) :
        queryset = Serviceuser.objects.all()
        serializer_class = ServiceuserSerializer
    ```

11. 프로젝트 폴더 > routers.py 생성
    ```
    # 주소와 보여질 데이터를 정의해 놓은 ServiceuserViewSet과 연결
    from rest_framework import routers
    from dogtest_app.viewsets import ServiceuserViewSet

    router = routers.DefaultRouter()

    # 주소는 localhost:8000/dogtest 로 시작하게 됨
    router.register(r'dogtest', ServiceuserViewSet)
    ```



12. 프로젝트 폴더 > urls.py에 코드 추가 
    ```
    from django.contrib import admin
    from django.urls import path, include

    from .routers import router

    urlpatterns = [
        path('admin/', admin.site.urls),

        # /api/dogtest 로 접속했을때 api-dogtest가 잘 작동하는지 테스트
        path('api/', include(router.urls)),
    ]
    ```

→→→→ 회원가입, 로그인 기능 구현

1. 회원가입 할 때 중복된 id가 있는지 확인하는 코드
    - 앱폴더 > views.py
    ```
    from django.views.decorators.csrf import csrf_exempt
     ...

    @csrf_exempt
    def signup( request ):
        # GET요청이 들어오면 사용자가 입력한 ID와 기존의 ID가 일치하는지 여부 검사
        if request.method == "GET" :
            data = JSONParser().parse(request)
            desired_id = data['user_id']
            # exist_id = Serviceuser.objects.get(user_id = desired_id)
            try : 
                if Serviceuser.objects.get(user_id = desired_id) :   # 존재하면
                    return HttpResponse(status=200)
            except:
                return HttpResponse(status=203)
    ```

2. POST방식으로 요청이 들어오면 회원가입 성공
   - 앱폴더 > views.py 의 def signup(request) : 에 추가
   ```
    elif request.method == "POST" :
            data = JSONParser().parse(request)
            data['user_pw'] = PasswordHasher().hash(data['user_pw'])
            serializer = ServiceuserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
   ```

    2-1. 비밀번호 암호화 방법
        - 장고는 암호 알고리즘을 이용한 암호화 함수를 기본적으로 제공
        - 장고에서는 해싱 알고리즘으로 `Argon2` 사용 권장
        - pip install argon2-cffi 

    2-2. 프로젝트 폴더 > settings.py에 PASSWORD_HASHERS 코드 추가 (안해도되는건가?)
        ```
        PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.Argon2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
            'django.contrib.auth.hashers.ScryptPasswordHasher',
        ]
        ```

    2-3. 앱 폴더 > views.py 에 PasswordHasher 임포트
        - import 추가하고 회원 생성하는 부분 수정
        ```
        from argon2 import PasswordHasher    
        ...
        def signup(request):
            ...
        
            elif request.method == "POST" :
            data = JSONParser().parse(request)
            data['user_pw'] = PasswordHasher().hash(data['user_pw'])
            serializer = ServiceuserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
    ```

3. 로그인 시 입력받은 비밀번호 일치여부를 확인하기 위해서는 PasswordHasher().verify()함수 이용
    - PasswordHasher().verify(암호화된 비밀번호, 입력받은 비밀번호)
    - 앱 폴더 > views.py 의 def login( request ) 함수 수정
    ```
    @csrf_exempt
    def login( request ):
        if request.method == "POST":
            data = JSONParser().parse(request)
            input_id,  input_pw = data['user_id'],  data['user_pw']
            user_data = Serviceuser.objects.get(user_id=input_id)
            # DB에 저장된 id와 pw가 입력한 id와 pw가 일치한다면 status = 200
            try : 
                if user_data.user_id == input_id and PasswordHasher().verify(user_data.user_pw, input_pw) :
                    return HttpResponse(status = 200)
            except : 
                return HttpResponse(status=400)
    ```

+) 테스트 확인을 위해 임시로 유저 리스트 확인과 삭제 코드도 만듦
    ``` 
    @csrf_exempt
    def user_list( request ) :
        # GET요청이 들어오면 전체 address list를 내려주는  
        if request.method == 'GET':
            query_set = Serviceuser.objects.all()
            serializer = ServiceuserSerializer(query_set, many=True)  # many옵션은 다수의 queryset형태를 serializer화 하고자 할 때 사용 
            return JsonResponse(serializer.data, safe=False)
        elif request.method == "DELETE":
            data = JSONParser().parse(request)
            user_data = Serviceuser.objects.get(user_id=data['user_id'])
            user_data.delete()
            return HttpResponse(status=200)
    ```


→→→→→  학습된 모델을 백엔드에 넣어야 함
1. 앱 폴더 > app.py
    - 









<!-- ----------------- Vue.js와 Django 연결 -----------------

1. 앱 폴더 안에 templates 폴더 생성 > 앱 폴더 생성 > index.html 파일 생성
    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <link rel="icon" href="<%= BASE_URL %>dog.ico">
        <title>강아지 정상/비만 판별기</title>
    </head>
    <body>
        <noscript>
        <strong>We're sorry but 강아지 정상/비만 판별기 doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
        </noscript>
        <div id="app"></div> 
    </body>
    </html>
    ```

2. 프로젝트 폴더 > urls.py 코드 업데이트
    ```
    from django.contrib import admin
    from django.urls import path, include

    from .routers import router
    from django.views.generic import TemplateView

    urlpatterns = [
        path('admin/', admin.site.urls),
        # /api/dogtest 로 접속했을때 api-dogtest가 잘 작동하는지 테스트
        path('api/', include(router.urls)),
        path('dogtest', TemplateView.as_view(template_name='dogtest/index.html')),    
    ]
    ```

3. `vuter` 라는 확장파일 설치 & 터미널에서 vue cli설치
    - npm install -g @vue/cli

4. 프로젝트 생성
    - vue create 프로젝트명 
        - 프로젝트명 : dogtest_web  / defalut로 설치

5. 생성된 프로젝트로 이동 후 서버가 잘 돌아가는지 확인
    - cd dogtest_web
    - npm run serve 

6. 생성한 프로젝트 파일 안에 소영님이 만드신 vue.js파일 복사하여 넣고 다시 실행
    - npm run serve


터미널에 npm install vue-router -save하니까 
package.json 의  dependencies : { ... , "vue-route": "^1.5.1",  ... } 가 추가됨 
- 여기서 -save는 package.json 파일에 자동으로 dependencies에 등록해주는 역할 -->