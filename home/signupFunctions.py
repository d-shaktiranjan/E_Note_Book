from home.models import UsersData
from random import randint


def checkMail(mail):
    return bool(UsersData.objects.filter(mail=mail))


def otpGenerate():
    range_start = 10**(6-1)
    range_end = (10**6)-1
    return randint(range_start, range_end)


def checkPic(request):
    if request.session.get('log'):
        aboutUser = UsersData.objects.filter(
            mail=request.session.get('mail')).first()
        about = {
            "allInfo": aboutUser,
            "isPic": False,
        }
        try:
            from os import listdir
            fileList = listdir("static/userImage")
            userList = []
            for file in fileList:
                tempList = file.split(".")
                userList.append(tempList[0])
            if request.session['userName'] in userList:
                about["isPic"] = True
                about["userName"] = fileList[userList.index(
                    request.session['userName'])]
        except:
            pass
    return about
