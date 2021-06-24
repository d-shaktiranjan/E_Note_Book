from django.shortcuts import render, redirect, HttpResponse
from home.views import index as homeIndex, error
from home.models import UsersData
from django.core.mail import send_mail
from django.conf import settings
from home.signupFunctions import otpGenerate
from django.contrib.auth.hashers import make_password
from forgotPass.models import ForgotTempData

from notebook.views import successMessage
# Create your views here.


def index(request):
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        mail = request.POST.get('email')
        userInfo = UsersData.objects.filter(
            mail=mail).first()
        if userInfo == None:
            return error(request, "Your mail is not registered to us", "Home", "/")
        otp = otpGenerate()
        try:
            send_mail(
                "OTP | E Note Book",
                f'Hey your OTP to reset password is {otp}',
                settings.EMAIL_HOST_USER,
                [mail],
                fail_silently=False,
            )
            tempUser = ForgotTempData(otp=otp, mail=mail)
            tempUser.save()
            userDict = {"mail": mail}
        except:
            return error(request, "There are some internal issue", "Home", "/")
        return render(request, "forgotOtpCheck.html", userDict)
    return render(request, "fIndex.html")


def otpcheck(request):
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        mail = request.POST.get('mail')
        userOtp = request.POST.get('otp')
        tempUserData = ForgotTempData.objects.filter(mail=mail).first()
        if userOtp == tempUserData.otp:
            userDict = {"mail": tempUserData.mail}
            tempUserData.delete()
            return render(request, "resetPassword.html", userDict)
        tempUserData.delete()
        return error(request, "OTP not matched", "Try Again", "/forgot")
    return render(request, "forgotOtpCheck.html")


def resetPass(request):
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        newPass = request.POST.get('newPass')
        newConPass = request.POST.get('newConPass')
        mail = request.POST.get('mail')
        if newConPass == newPass:
            userInfo = UsersData.objects.filter(
                mail=mail).first()
            userInfo.password = make_password(newPass)
            userInfo.save()
            return successMessage(request, "Password reset done", "Home", "/")
        return error(request, "New password & confirm password not matched", "Try Again", "/forgot")
    return redirect(index)
