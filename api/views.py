# api/views.py
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets
from .serializers import PlantSerializer, DataSerializer
from .models import Plant, Data
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from django.templatetags.static import static
import os
import json
# Create your views here.


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


# 측정값 받아와서 Data Table에 저장하는 메서드
@csrf_exempt
def measure(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('received data: ' + str(data))

        serial_num = data.get('plant_id')
        data_light = data.get('light')
        data_temp = data.get('temp')
        data_humi = data.get('humi')
        data_watery = data.get('watery')
        data_ph = data.get('ph')

        try:
            plant = Plant.objects.get(pk=serial_num)
        except Plant.DoesNotExist:
            print("deny: Plant DoesNotExist")
            return JsonResponse({
                'status_code': 403,
                'error': 'The serial number was not found'
            })
        else:
            try:
                last_data = Data.objects.filter(plant_id=plant).last()
            except IndexError:
                pass
            else:
                if not last_data:
                    pass
                elif int(last_data.watery) < 50 < int(data_watery):
                    plant.date_watered = timezone.now()
                    plant.save()
            Data.objects.create(plant_id=plant, light=data_light, temp=data_temp, humi=data_humi,
                                watery=data_watery, ph=data_ph, date_measured=timezone.now())
            return JsonResponse({
                'status_code': 201,
                'message': 'Object created'
            })

    elif request.method == 'GET':
        # GET method not allowed
        return HttpResponse('GET method not allowed')
    else:
        return HttpResponse('404 page not found')


# 이미지 업로드 하는거 받아서 jpg 파일 저장하는 메서드
@csrf_exempt
def uploadimages(request, count):
    # 이미지 파일 이름 만들기
    if request.method == 'POST':
        body = json.loads(request.body)
        serial_num = body.get('plant_id')

        try:
            Plant.objects.get(pk=serial_num)
        except Plant.DoesNotExist:
            print('/uploadimages/ deny : serial not found')
            return JsonResponse({
                'status_code': 404,
                'error': 'The serial number was not found'
            })

        plant = Plant.objects.get(pk=serial_num)    # Plant 객체 불러오기
        uid = plant.master_id.id
        img_count = plant.image_count + 1
        filename = 'IMG_' + str(img_count).zfill(4) + '.jpg'  # 파일명
        # filepath = 현재 프로세스의 작업 디렉토리 + 파일경로... 로컬서버 아닐땐 수정하기!!!!
        filepath = os.getcwd() + '/static/' + str(uid) + '/' + serial_num + '/images/'
        # 파일 쓰기
        try:
            # 중간에 끊겼다가 다시 들어오면 파일 새로 만들기
            if count == 1:
                f = open(os.path.join(filepath, filename), 'wb')
            else:
                f = open(os.path.join(filepath, filename), 'ab')
        except FileNotFoundError:
            try:
                os.makedirs(os.path.join(filepath))
            except FileExistsError:
                pass
            f = open(os.path.join(filepath, filename), 'wb')
        data = body.get('data')
        f.write(bytes.fromhex(data))
        f.close()
        # 마지막 전송이면 image_count 증가
        if count == 0:
            plant.image_count = img_count
            plant.save()
            # 201 Created
            return JsonResponse({
                'status_code': 201,
            })
        else:
            # 100 Continue
            return JsonResponse({
                'status_code': 100,
            })

    else:   # POST 아닐 때
        return HttpResponse('404 page not found')


# 아두이노 전원 켤 때 들어오는 요청, Plant에 등록되어있는지 확인, 촬영주기 반환 (jsonResponse)
@csrf_exempt
def join(request):
    # serial_num = request.POST.get('plant_id')
    # print(list(request.POST.items()))
    # print(str(request.body))

    data = json.loads(request.body)
    serial_num = data.get('plant_id')
    print('received serial_num: '+str(serial_num))

    try:
        plant = Plant.objects.get(pk=serial_num)
    except Plant.DoesNotExist:
        print("deny: Plant DoesNotExist")
        return JsonResponse({
            'status_code': 403,
            'error': 'The serial number was not found'
        })
    else:
        plant = Plant.objects.get(pk=serial_num)
        period = plant.timelapse_period
        return JsonResponse({
            'status_code': 200,
            'timelapse_period': period
        })
