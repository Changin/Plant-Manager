from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, FileResponse
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from api.models import Plant, Data
from openai import OpenAI
from django.utils import timezone
import os
import json
import pandas as pd
import time

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file, 'r') as f:   # open as로 secret.json을 열기
    secrets = json.loads(f.read())


def get_secret(setting, secrets = secrets):   # 예외 처리를 통해 오류 발생을 검출합니다.
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


system_instructions = get_secret("INSTRUCTIONS")
openai_api_key = get_secret("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key
client = OpenAI()


def get_completion(prompt, model="gpt-4o-mini"):
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=512,
    )
    return response.choices[0].message.content


# Openai API 연결, 응답 반환 함수
def get_answer(parameters):
    prompt = '오늘 날짜 : ' + parameters['today'] + ', 식물 이름 : ' + parameters['name'] + ', 최근 물 준 날짜 : ' + str(parameters['date_watered']) + ', 현재 토양습도(%) : ' + parameters['current_watery']
    prompt += ', 30일 평균치 = { 온도(섭씨): ' + parameters['avg_temp'] + ', 조도(%): ' + parameters['avg_light']
    prompt += ', 대기습도: ' + parameters['avg_humi'] + ', 토양습도: ' + parameters['avg_watery'] + '}\n'
    prompt += '질문 또는 문제상황 : ' + parameters['prompt']
    response = get_completion(prompt)
    return response


def chatbotmain(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')

    try:
        plants = Plant.objects.filter(master_id=request.user)
    except Plant.DoesNotExist:
        plants = None

    return render(request, 'chatbot/chatbotmain.html', {'plants': plants})


def get_response(request):
    # 로그인 후 이용 가능
    if not request.user.is_authenticated:
        return redirect('/users/login')

    # 요청받은 식물의 시리얼넘버 파싱
    serial_num = request.GET.get('serial')
    if serial_num is None:
        return redirect('/home')

    # Plant 객체 못 찾을 때 예외 처리
    try:
        plant = Plant.objects.get(pk=serial_num)
    except Plant.DoesNotExist:
        return redirect(reverse('home:index'))

    # 로그인한 사용자에 대한 요청이 아닌 경우
    if request.user.pk is not plant.master_id.pk:
        return redirect(reverse('home:index'))

    # 파라미터 및 최근 30시간 (나중에 30일 24*30 = 720시간 바꾸기) 평균 데이터 뽑기
    iter_time = 30  # 720 : 30일
    datas = Data.objects.filter(plant_id=plant).order_by('-date_measured')
    light_sum = temp_sum = humi_sum = watery_sum = 0
    if len(datas) == 0:
        return JsonResponse({'answer': 'No datas'})
    elif len(datas) < iter_time:   # 30개 미만인 경우
        iter_time = len(datas)
        for data in datas:
            light_sum += int(data.light)
            temp_sum += float(data.temp)
            humi_sum += float(data.humi)
            watery_sum += int(data.watery)
    else:  # 30개 이상일 경우 30번만 계산
        for i in range(iter_time):
            light_sum += int(datas[i].light)
            temp_sum += float(datas[i].temp)
            humi_sum += float(datas[i].humi)
            watery_sum += int(datas[i].watery)

    avg_light = light_sum / iter_time
    avg_temp = temp_sum / iter_time
    avg_humi = humi_sum / iter_time
    avg_watery = watery_sum / iter_time

    current_data = datas[0]

    # GPT 질의, 응답 결과 가져오기
    prompt = request.GET.get('prompt')
    parameters = {
        'today': str(timezone.now()),
        'prompt': prompt,
        'name': plant.name,
        'date_watered': plant.date_watered,
        'current_watery': current_data.watery,
        'avg_light': str(avg_light),
        'avg_temp': str(avg_temp),
        'avg_humi': str(avg_humi),
        'avg_watery': str(avg_watery)
    }
    answer = get_answer(parameters)
    return JsonResponse({'answer': answer})
