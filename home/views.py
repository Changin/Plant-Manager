from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from api.models import Plant, Data    # 오류 안뜸


# Create your views here.
def index(request):
    # return HttpResponse("/home home page")
    if request.user.is_authenticated:   # 로그인한 경우 식물리스트 주기
        try:
            plants = Plant.objects.filter(master_id=request.user)
        except Plant.DoesNotExist:
            plants = None
    else:   # 로그인 안되어있는 경우 일반 홈 화면 렌더링
        plants = None
    return render(request, "home/index.html", {"plants":plants})


def newplant(request):
    # return HttpResponse("/home/newplant/ : 새 식물 추가 페이지입니다.")
    if request.user.is_authenticated:
        return render(request, "home/newplant.html")
    else:
        return redirect('/users/login/')


# 새 식물 추가 폼 받아서 객체 생성하는 메서드
def newplantsubmit(request):
    plant = None
    if request.user.is_authenticated and request.method == 'POST':
        serial_num = request.POST['serial_num']
        name = request.POST['name']
        nickname = request.POST['nickname']
        date_watered = request.POST['date_watered']
        master_id = request.user
        timelapse_path = '/static/'+str(master_id.id)+'/' + serial_num + '/images/'
        Plant.objects.create(
            master_id=master_id,
            serial_num=serial_num,
            name=name,
            nickname=nickname,
            date_watered=date_watered,
            timelapse_path=timelapse_path
        )
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return redirect(reverse('home:index'))


# 식물 정보 출력, 타입랩스 링크, 최근 업데이트된 측정값 출력
def detail(request):
    if request.user.is_authenticated:
        serial_num = request.GET.get('serial_num')
        if serial_num is None:
            return HttpResponseRedirect(reverse('home:index'))

        # TODO: 객체 못찾았을때 예외처리 하기
        plant = Plant.objects.get(pk=serial_num)
        datas = Data.objects.filter(plant_id=plant)

        if len(datas) is 0:
            current_data = None
        else:
            current_data = datas[len(datas) - 1]

        return render(
            request,
            'home/detail.html',
            {'plant': plant, 'current_data': current_data}
        )
    else:
        return HttpResponseRedirect(reverse('home:index'))


def timelapse(request):
    if request.user.is_authenticated:
        serial_num = request.GET.get('serial_num')
        if serial_num is None:
            return HttpResponseRedirect(reverse('home:index'))
        plant = Plant.objects.get(pk=serial_num)
        # datas = Data.objects.filter(plant_id=plant)
        return render(
            request,
            'home/timelapse.html',
            {'plant': plant}
        )
    else:
        return HttpResponseRedirect(reverse('home:index'))


def setperiod(request):
    plant = None
    if request.user.is_authenticated:
        period = request.POST['period']
        serial_num = request.GET.get('serial_num')
        plant = Plant.objects.get(pk=serial_num)
        plant.timelapse_period = period
        plant.save()
        return HttpResponseRedirect(reverse('home:timelapse')+'?serial_num='+serial_num)
    else:
        return redirect(reverse('home:timelapse'))


def data(request):
    if request.user.is_authenticated:
        serial_num = request.GET.get('serial_num')
        if serial_num is None:
            return HttpResponseRedirect(reverse('home:index'))
        plant = Plant.objects.get(pk=serial_num)
        datas = Data.objects.filter(plant_id=plant)
        return render(
            request,
            'home/data.html',
            {'plant': plant, 'datas': reversed(datas)}
        )
    else:
        return HttpResponseRedirect(reverse('home:index'))