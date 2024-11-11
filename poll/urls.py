from django.urls import path
from . import views

app_name = 'poll'
urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path("survey/", views.survey, name="survey"),
    path("result/", views.result, name="result")
]