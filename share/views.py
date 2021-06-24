from django.shortcuts import render, HttpResponse

# Create your views here.


def share(request, slug):
    return HttpResponse("Share Page")


def makePublic(request):
    return HttpResponse("URL TEST")
