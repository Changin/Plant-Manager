"""
URL configuration for plant_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("users/", include("users.urls")),
    path("home/", include("home.urls")),  # home 앱의 urls 연결
    path("", include("home.urls")),
    path("api/", include("api.urls")),  # rest api
    path("poll/", include("poll.urls")),  # polls
    path("chatbot/", include("chatbot.urls")),  # chatbot
    path('admin/', admin.site.urls),
]