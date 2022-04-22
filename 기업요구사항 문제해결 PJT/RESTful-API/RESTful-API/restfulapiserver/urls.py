"""restfulapiserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from addresses import views  # addresses안에 views를 import 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # addresses/ 라는 url이 오면 address_list를 실행
    path('addresses/', views.address_list),
    path('addresses/<int:pk>', views.address),
    path('login/', views.login),
]




# #### 공식 홈페이지 sample 코드
# from django.urls import path, include
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets

# # Serializers define the API representation.
# # Django rest framework에서 제공하는 Serializer는
# # Database에서 우리가 사용하고자하는 특정 모델과 column을 명시해주면
# # Serializer는 응답을 주기 편하게 선택된 column에 대해서만 data를 JSON형태로 바꿔주는 역할을 함 
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# # ViewSets define the view behavior.
# # 유저들을 호출하면 UserViewSet을 실행시킴
# # UserViewSet은 queryset을 생성
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()   # User모델에 있는 모든 내용을 queryset으로 생성
#     serializer_class = UserSerializer  # 응답은 JSON형태로 할 것이기 때문에 UserSerializer를 씀

# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# # GET을 호출하면 UserViewSet 메소드 클래스가 실행이 되고 
# router.register(r'users', UserViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]