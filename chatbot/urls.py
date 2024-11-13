from django.urls import path
from . import views

app_name = "chatbot"
urlpatterns = [
    path("", views.chatbotmain, name='chatbotmain'),
    path("get_response/", views.get_response, name='getresponse')
]