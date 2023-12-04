from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name='index'),
    path("newplant/", views.newplant, name="newplant"),
    path("newplantsubmit/", views.newplantsubmit, name='newplantsubmit'),
    path("detail/", views.detail, name='detail'),
    path('detail/timelapse/', views.timelapse, name='timelapse'),
    path('detail/timelapse/setperiod/', views.setperiod, name='setperiod'),
    path('detail/data/', views.data, name='data'),
]