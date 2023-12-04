from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter() # DefaultRouter를 설정
router.register('Plant', views.PlantViewSet)    # plantviewset 과 plant router 등록
router.register('Data', views.DataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('measure/', views.measure, name='measure'),
    path('uploadimages/<int:count>/', views.uploadimages, name='uploadimages'),
    path('join/', views.join, name='join'),
]