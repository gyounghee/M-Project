from django.urls import path
from . import views

urlpatterns = [    
    ### login page가 따로 있지 않고, 초기 페이지에서 login이 가능하도록 하신거 같아서 url설정 따로 안함
    path('', views.login, name='mainpage'),
    path('signup/', views.signup, name='signup'),
    path('dogimage/', views.imageupload, name='dogimage'),
    path('testresult/',views.testresult, name='testresult'),

    # # 테스트 확인용 ( 조회, 삭제 ) 
    # path('users/', views.user_list), 
    # path('testresults/', views.testresult_list),

    
]