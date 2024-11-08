from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.files.storage import FileSystemStorage
from api.models import Plant, Data    # 오류 안뜸
from django.core.paginator import Paginator     # 페이징을 위한 Paginator
from PIL import Image
import PIL
import cv2
import os
import io
import numpy


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
    return render(request, "home/index.html", {"plants": plants})

def about(request):
    # return HttpResponse("this is about page")
    return render(request, "home/about.html")

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    serial_num = request.GET.get('serial_num')
    if serial_num is None:
        return HttpResponseRedirect(reverse('home:index'))

    # 객체 못 찾았을 때 예외 처리
    try:
        plant = Plant.objects.get(pk=serial_num)
    except Plant.DoesNotExist:
        return redirect(reverse('home:index'))

    # 해당 사용자의 식물이 아닌 경우
    if request.user.pk is not plant.master_id.pk:
        return HttpResponseRedirect(reverse('home:index'))

    # 최근 데이터 선별, 렌더링
    datas = Data.objects.filter(plant_id=plant)
    if len(datas) == 0:
        current_data = None
    else:
        current_data = datas[len(datas) - 1]

    return render(
        request,
        'home/detail.html',
        {'plant': plant, 'current_data': current_data}
    )


def timelapse(request):
    # 사진 보기 페이지
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    serial_num = request.GET.get('serial_num')
    if serial_num is None:
        return HttpResponseRedirect(reverse('home:index'))

    # 객체 못 찾았을 때 예외 처리
    try:
        plant = Plant.objects.get(pk=serial_num)
    except Plant.DoesNotExist:
        return redirect(reverse('home:index'))

    # 해당 사용자의 식물이 아닌 경우
    if request.user.pk is not plant.master_id.pk:
        return HttpResponseRedirect(reverse('home:index'))

    page = request.GET.get('page', '1')  # 페이지, 디폴트 1

    # 이미지 카운트에 맞게 이름 리스트 뽑기, 렌더링
    # ToDo : 이미지 DB 추가하여 더 Nice한 방법으로 리팩터링하기
    images = []
    for i in range(plant.image_count):
        images.append('IMG_' + str(i+1).zfill(4) + '.jpg')
    images.reverse()    # 이미지 최신순 정렬
    paginator = Paginator(images, 18)  # 페이지 당 18개씩
    page_obj = paginator.get_page(page)
    return render(
        request,
        'home/timelapse.html',
        {'plant': plant, 'images': page_obj}
    )


def setperiod(request):
    plant = None
    if request.user.is_authenticated:
        period = request.POST['period']
        serial_num = request.GET.get('serial_num')
        plant = Plant.objects.get(pk=serial_num)
        plant.timelapse_period = period
        plant.save()
        return HttpResponseRedirect(reverse('home:detail')+'?serial_num='+serial_num)
    else:
        return redirect(reverse('home:index'))


def download(request):
    plant = None
    if request.user.is_authenticated:
        serial_num = request.GET.get('serial_num')
        try:
            plant = Plant.objects.get(pk=serial_num)
        except Plant.DoesNotExist:
            return redirect(reverse('home:detail')+'?serial_num='+serial_num)

        if plant.image_count < 15:
            return redirect(reverse('home:detail')+'?serial_num='+serial_num)

        image_folder = os.getcwd()+plant.timelapse_path
        video_folder = image_folder+'/video/'
        video_name = image_folder+'/video/video.mp4'
        try:
            os.makedirs(video_folder)
        except FileExistsError:
            pass
        create_timelapse(image_folder, video_name)

        fs = FileSystemStorage(video_folder)
        try:
            response = FileResponse(fs.open(video_name, 'rb'),
                                    content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="video.mp4"'
        except FileNotFoundError:
            response = HttpResponseRedirect(reverse('home:detail')+'?serial_num='+serial_num)
        return response

    else:
        return redirect(reverse('home:index'))


def create_timelapse(image_folder, video_name):
    # 1. 모든 이미지 파일의 파일명을 리스트로 변환
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()
    images.pop()    # 마지막 이미지 제외
    print(images)

    # 2. 첫번째 이미지의 프레임크기 정보를 가져온다.
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    print(width, height, layers)

    # 3. 비디오 생성, 3번째 Argument - Frame rate 조절
    # *은 'D', 'I', 'V', 'X' 이렇게 문자열을 문자로
    video = cv2.VideoWriter(video_name,
                            cv2.VideoWriter_fourcc(*'DIVX'),
                            10,
                            (width, height))

    # 4. 이미지 파일을 하나씩 가져와서 비디오에 추가
    img = None
    for image in images:
        with open(os.path.join(image_folder, image), 'rb') as img_bin:
            # cv2.imread 하면 일부 깨져있는 이미지 로드할때 오류가 터져서 numpy로 read
            buff = io.BytesIO()
            buff.write(img_bin.read())
            buff.seek(0)
            temp_img = numpy.array(PIL.Image.open(buff), dtype=numpy.uint8)
            img = cv2.cvtColor(temp_img, cv2.COLOR_RGB2BGR)
            video.write(img)
    # 5. 종료
    cv2.destroyAllWindows()
    video.release()


def data(request):
    # 측정값 전체 보기
    # 로그인 되어 있지 않은 경우 홈으로
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    page = request.GET.get('page', '1')     # 페이지, 디폴트 1
    serial_num = request.GET.get('serial_num')

    # 없는 식물에 대한 요청인 경우
    if serial_num is None:
        return HttpResponseRedirect(reverse('home:index'))

    # 객체 못 찾았을 때 예외 처리
    try:
        plant = Plant.objects.get(pk=serial_num)
    except Plant.DoesNotExist:
        return redirect(reverse('home:index'))

    # 해당 사용자의 식물이 아닌 경우
    if request.user.pk is not plant.master_id.pk:
        return HttpResponseRedirect(reverse('home:index'))

    # 데이터 정렬, 렌더링
    datas = Data.objects.filter(plant_id=plant).order_by('-date_measured')
    paginator = Paginator(datas, 12)  # 페이지 당 12개씩
    page_obj = paginator.get_page(page)
    context = {'plant': plant, 'datas': page_obj}
    return render(
        request,
        'home/data.html',
        context
    )