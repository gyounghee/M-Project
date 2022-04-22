from tkinter import CASCADE
from django.db import models
from django import forms

### 코드로 테스트하는 방법  유니테스트라던가..(구현 후 시간이 남으면 )

# Create your models here.
class Serviceuser(models.Model) : 
    # user_id = models.CharField(max_length=15, primary_key=True)
    # user_pw = models.CharField(max_length=225)
    userid = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=225, null=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']

# 사용자, 이미지 이름, 견종, 결과, 테스트시각
class Testresult(models.Model) :
    # userid =  models.ForeignKey(Serviceuser, on_delete=models.PROTECT)
    userid = models.CharField(max_length=20)
    image = models.CharField(max_length=255,blank=True)  # 이미지명 저장
    dog_breed = models.CharField(max_length=100)
    testresult = models.CharField(max_length=255)
    accuracy = models.CharField(max_length=10, blank=True)
    like = models.IntegerField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created']