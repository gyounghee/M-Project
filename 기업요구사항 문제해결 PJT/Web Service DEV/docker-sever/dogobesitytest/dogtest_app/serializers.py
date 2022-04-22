from rest_framework import serializers
from .models import Serviceuser, Testresult

class ServiceuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serviceuser 
        # fields = ['user_id','user_pw','created']
        fields = ['userid','password','created']

class TestresultSerializer(serializers.ModelSerializer):
    # userid = ServiceuserSerializer()
    class Meta:
        model = Testresult
        # fields = ['userid','image_path','dog_breed','test_result','created'],
        fields = ['userid','image','dog_breed','testresult','accuracy', 'like','created']

