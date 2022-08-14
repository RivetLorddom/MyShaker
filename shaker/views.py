from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, "shaker/index.html")

def favorites(request):
    return HttpResponse("my favorites")