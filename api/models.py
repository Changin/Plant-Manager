from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Plant(models.Model):
    serial_num = models.CharField(max_length=100, unique=True, primary_key=True)    # 제품 S/N, PK
    master_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 소유자 uid
    name = models.CharField(max_length=50) # 식물 종
    nickname = models.CharField(max_length=20) # 식물 별명
    date_watered = models.DateField("watered date") # 최근 물준 날짜
    timelapse_period = models.IntegerField(default=12) # 타임랩스 촬영 주기 (단위 : 시간)
    timelapse_path = models.CharField(max_length=100) # 타임랩스 폴더 경로 static/uid/식물id/images
    image_count = models.IntegerField(default=0) # 보유 이미지 count

    def __str__(self):
        msg = str(self.nickname) + '@' + str(self.serial_num)
        return msg


class Data(models.Model):
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE) # 식물 id
    date_measured = models.DateTimeField("measured date", default=timezone.now()) # 측정일시
    light = models.CharField(max_length=10)  # 조도값
    temp = models.CharField(max_length=10)  # 온도값
    humi = models.CharField(max_length=10)  # 습도값
    watery = models.CharField(max_length=10)    # 토양수분값
    ph = models.CharField(max_length=10, null=True)    # 산성도값
    is_img_exist = models.BooleanField(default=False) # 이 시간대 이미지 있는지
