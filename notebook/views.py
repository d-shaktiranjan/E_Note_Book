from django.shortcuts import render


def successMessage(request, successMsg, buttonName, buttonLink):
    successDict = {
        "msg": successMsg,
        "name": buttonName,
        "link": buttonLink
    }
    return render(request, "success.html", successDict)
