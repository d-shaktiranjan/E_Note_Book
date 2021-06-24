from django.shortcuts import render, HttpResponse

# Create your views here.


def makePublic(request):
    return HttpResponse("URL TEST")
