from rest_framework import serializers
from .models import Plant, Data


# 데이터 리스트 출력할때 json 포맷
class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"
