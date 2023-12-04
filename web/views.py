from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("/web home page")
    return render(request, "web/index.html")