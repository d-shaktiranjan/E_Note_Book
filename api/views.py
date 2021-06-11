from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
# Create your views here.


def userCheck(request):
    mail = request.GET.get('m')
    userDict = {
        "mail": mail,
        "status": None
    }
    return JsonResponse(userDict)
