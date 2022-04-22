* docker를 사용하는 이유
    1. docker를 이용하여 컨테이너를 만들면 이미지로 따로 만들 수 있어서 aws ec2가 우분투가 아닌 새로 만든 서버에 쉽게 옮겨서 사용 가능함 즉, 쉽게 서버 배포 가능
    2. 서비스가 확장되어 서버를 늘려야할 때 그 이미지를 복사해서 설치만하면 되기 때문에 편리
    3. 관리하는 툴인 오케스트라가 여러가지 도구가 많아서 쉽게 배포, 관리가 가능

* 전체적인 구조
- Web Client 
    - Djagno 서버로 API를 호출하는 앱 또는 웹
- Web Server
    - client로부터 request를 받아 뒤에 웹 어플리케이션으로 전달하고, 그에 대한 response를 다시 client로 전달하는 역할
    - ex) Nginx, apache, ... 등
- Socket 
    - Web Server와 WSGI 사이에는 Socket이 있는데 이는 Web Server와 WSGI 사이에 데이터를 주고 받기 위한 인터페이스로 사용된다.
    - Socket은 네트워크를 사용한 HTTP 소켓이 될 수도 있고, 파일을 사용한 소켓(Linux전용)이 될 수도 있음
- WSGI ( Web Server Gateway Interface )
    - Web Server와 Web Framework 사이에 통신을 담당하는 인터페이스로 Web Server와 Django사이에 통신을 담당
    - WSGI의 종류는 여러 가지가 있는데, 내가 지금 사용할 것은 uWSGI
        - WSGI는 개념이고, 그것을 구현한 것 중 하나가 uWSGI임.
- Django
    - 보안이 우수하고 유지보수가 편리한 웹 사이트를 신속하게 개발하도록 도움을 주는 Python Web Framework

_________________________________________________________________________________
Docker 사용하여 Nginx와 Django 띄우기
- Nginx , Django의 이미지를 따로 만들고자함
- 관리는 동시에 관리하기 위해 docker-compose  툴 사용
_________________________________________________________________________________

**Django docker화**
1. Putty 접속 후 
2. mkdir docker-server  ( 폴더 생성 ) 
3. cd docker-server 
- 이게 docker-compose의 root가 될 경로
- 여기에 Nginx 폴더랑 docker이미지 따로 Django폴더랑 docker이미지 따로 만들 예정
4. django 앱 다운받기
- git에 올렸던 프로젝트 파일 git clone git_repository_주소(나는 try repository였음)
- cd 폴더로 들어가기  (cd try)

5. docker 설치
- su로 들어가서 
- curl -fsSL https://get.docker.com/ | sudo sh
- 항상 docker설치 후 docker에 대한 권한을 현재 사용자한테 허가해줘야함 
- sudo usermod -aG docker $USER  
	- 저렇게 했는데 lab16유저에 권한 할당이 안돼서
	- 다시 su로 들어가서 usermod -aG docker lab16  해줬더니 됨 
    - su 에서 유저로 빠져나와서 id로 도커권한이 할당 되었는지 확인
- 권한을 주고 바로 적용안되고 껐다 켜야 적용되는 것 같음 아닐수도~


6. 
- Putty 재접속 후 
- cd docker-server
- cd try
- vi Dockerfile
- vi Dockerfile에 insert 해줘야함
```
FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim
RUN apt-get -y install libgl1-mesa-glx

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#EXPOSE 9000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
```
- esc 하고 wq! 하여 빠져나옴

7. 
- docker build -t try/django .  ( Dockerfile이 있는 docker-server 경로에서 실행)
- docker image ls  하여 확인

8. 만들어진 이미지 실행
- docker run try/django [ x ]

9.  데몬형태..?로 실행
- docker run -d try/django [ x , port mapping옵션 필요 ]
	- 현재 터미널에서 실행되는 것이 아닌 background에서 실행
	- 실행 멈출때는 docker stop 31bc1fb13c76  (docker stop CONTAINER_ID)
- docker ps
	- 실행중인 docker이미지 확인
- docker run을 할 때 local server의 port와 docker의 port와 매핑해주는 작업 필요
	- 우분투 서버에 9000번으로 들어오는 포트를 docker의 9000번 포트와 연결시키겠다는 옵션 필요
	- docker run -p 9000:9000 -d try/django  ( 연결성공 )
- docker stop f6c6815c979f  ( docker stop CONTAINER_ID )

_________________________________________________________________________________
Nginx를 띄우고 Nginx랑 dockerfile이랑 같이 할 docker-compose 만드는 작업
_________________________________________________________________________________ 

1. Django app애서 Nginx와 Django를 연결시키기 위해 uwsgi 설치
- vi requirements.txt 에 uwsgi 추가
```
uwsgi
```
esc로 빠져나오고 wq! 로 변경한거 저장

+) Dockefile에서 
- 이 두 부분은 필요 없음 (runserver로 띄울 것이 아니기 때문)
```
#EXPOSE 9000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
```
2. vi uwsgi.ini  파일 생성
```
[uwsgi]
socket = /srv/docker-server/django.sock
master = true

processes = 1
threads = 2

chdir = /srv/docker-server
module = dogtest.wsgi

logto = /var/log/uwsgi/uwsgi.log
log-reopen = true

vacuum = true
```
esc  :wq! 

- cd ..  (docker-server 경로에 있도록)

3. docker-compose 설치
: docker-compose는 docker를 관리하는 툴 설치
	- su   로 들어가서
	- curl -L https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
- 이 또한 마찬가지로 권한을 줘야 함
	- chmod +x /usr/local/bin/docker-compose

________________________________________________________________________________
Nginx 만들기
_________________________________________________________________________________
- mkdir nginx   ( 우선 폴더 생성 )
- cd nginx

5. nginx를 띄우는데 3가지 config 필요 (하나의 Dockerfile와 두 개의 nginx config)
- vi nginx.conf
```
user root;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    # multi_accept on;
}

http {

    ##
    # Basic Settings
    ##

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;
    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ##
    # SSL Settings
    ##

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
    ssl_prefer_server_ciphers on;

    ##
    # Logging Settings
    ##

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    ##
    # Gzip Settings
 ##

    gzip on;
    gzip_disable "msie6";

    # gzip_vary on;
    # gzip_proxied any;
    # gzip_comp_level 6;
    # gzip_buffers 16 8k;
    # gzip_http_version 1.1;
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    ##
    # Virtual Host Configs
    ##

    # include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```
- vi nginx-app.conf   ( 실제 django에 대한 서버 정의가 되어있는 )
```
upstream uwsgi {
    server unix:/srv/docker-server/django.sock;   # 아까 적은 socket이름 적으면 됨
}

server {
    listen 8900;
    server_name localhost;
    charset utf-8;
    client_max_body_size 128M;

    location / {
        uwsgi_pass      uwsgi;
        include         uwsgi_params;
    }

    location /media/ {
        alias /srv/docker-server/.media/;
    }

    location /static/ {
        alias /srv/docker-server/.static/;
    }
}
````

- vi Dockerfile
```
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

EXPOSE 8900
CMD ["nginx", "-g", "daemon off;"]
```
esc    :wq!

- docker-compose를 사용하기 전에 그냥 nginx만 docker로 사용해봄
 	- docker build -t try/nginx .
	- docker image ls 
	- docker run -d -p 8900:8900 try/nginx

________________________________________________________________________________
docker-compose 만들기
: docker 이미지를 각각 만들고나서  같이 띄워주는 역할
_________________________________________________________________________________
 
1. docker-compose.yml로 전체 환경을 관리
- 경로는 docker-server 파일안에서 
- vi docker-compose.yml
```
version : '3'

services:

    nginx:
        container_name: nginx
        build: ./nginx
        image: docker-server/nginx
        restart: always
        ports:
            - "8900:8900"
        volumes :
            - ./try:/srv/docker-server
            - ./log:/var/log/nginx
        depends_on:
            - django

    django:
        container_name: dajngo
        build: ./try
        image: docker-server/django
        restart: always
        command : uwsgi --ini uwsgi.ini
        volumes :
            - ./try:/srv/docker-server
            - ./log:/var/log/uwsgi
```
esc   :wq!   ( docker-compose 완료 )


2. docker-compose를 사용해서 docker image가 생성되는지 확인하기 위해 기존의 이미지 모두 삭제  
-  docker image rm --force  이미지_ID

3. docker-compose 실행
- docker-compose up -d --build  (데몬모드로 실행되고 이미지 생성)

3-1. docker-compose 끌 때는
- docker-compose down 

4. 잘 실행되는지 확인하려면
- docker-compose ps
	- django 가 Restarting 이 뜸.  왜 죽는지 확인  → uwsgi.ini 파일에서 오타 발견 (해결)

8900 port로 잘 접속되는거 성공
____________________________________________________________________
docker-compose로 docker를 이용한 nginx이미지 django 이미지를 aws ec2 ubuntu에 올리는 작업 성공
____________________________________________________________________

**source code가 계속 업데이트 될 경우**
1. django 웹 폴더에 가서 git을 만들어서 
2. git pull 해주면 됨 (재빌딩을 하지 않아도 됨)
