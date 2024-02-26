from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name='index'),
    path("newplant/", views.newplant, name="newplant"),
    path("newplantsubmit/", views.newplantsubmit, name='newplantsubmit'),
    path("detail/", views.detail, name='detail'),
    path('timelapse/', views.timelapse, name='timelapse'),
    path('setperiod/', views.setperiod, name='setperiod'),
    path('download/', views.download, name='download'),
    path('data/', views.data, name='data'),
]