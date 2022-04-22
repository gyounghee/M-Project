# rest framework에서 serializer를 가져와야함
from rest_framework import serializers
# models.py에서 만든 모델(DB)를 불러올 것이기 때문에 import
# models.py와 serializers.py가 같은 폴더이기 떄문에 .(현재경로의)models 
from .models import Addresses    

class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ['name','address','created']

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Addresses.objects.create(**validated_data)
