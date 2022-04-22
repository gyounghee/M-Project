from email.headerregistry import Address
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Addresses
from .serializers import AddressesSerializer


# Create your views here.
@csrf_exempt
def address_list( request ) :
    # GET요청이 들어오면 전체 address list를 내려주는  
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)  # many옵션은 다수의 queryset형태를 serializer화 하고자 할 때 사용 
        return JsonResponse(serializer.data, safe=False)
    
    # POST 요청이 들어오면 만들어주는
    elif request.method == 'POST':
        # 클라이언트에서 불러온 데이터를 JSON 파싱해서 넣음
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        # 클라이언트에서 올린 데이터와 우리가 만든 모델 filed의 데이터와 동일하면
        # 즉. client에서 올린 데이터가 정상적으로 잘 올라왔다면 
        if serializer.is_valid() :    
            serializer.save()   # 저장  →  
            return JsonResponse(serializer.data, status=201)  # 어떤 데이터가 잘 만들어졌다는 응답
        return JsonResponse(serializer.errors, status=400)  # 에러 났다는 응답을 줌


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