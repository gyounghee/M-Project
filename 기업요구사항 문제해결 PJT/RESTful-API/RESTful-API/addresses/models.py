from django.db import models

# Create your models here.

class Addresses(models.Model): 
    name = models.CharField(max_length=10)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    # class Meta는 선택사항
    class Meta:
        # 조회 시 created를 기준으로 내림차순으로 표시됨 (순서대로 표시하기 위함)
        ordering = ['created']