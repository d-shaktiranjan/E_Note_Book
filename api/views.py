from django.http import JsonResponse
from home.signupFunctions import checkMail
# Create your views here.


def userCheck(request):
    mail = request.GET.get('m')
    userDict = {
        "mail": mail,
        "status": None
    }
    if mail == None:
        return JsonResponse(userDict)
    userDict["status"] = checkMail(mail)
    return JsonResponse(userDict)
