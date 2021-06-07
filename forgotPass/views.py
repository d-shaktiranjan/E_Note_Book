from django.shortcuts import render, redirect, HttpResponse
from home.views import index as homeIndex, error
from home.models import UsersData
from django.core.mail import send_mail
from django.conf import settings
from home.signupFunctions import otpGenerate
from django.contrib.auth.hashers import make_password

# Create your views here.

GLOBAL_otp = ""
GLOBAL_email = ""
GLOBAL_match = False


def index(request):
    global GLOBAL_email, GLOBAL_otp
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        email = request.POST.get('email')
        userInfo = UsersData.objects.filter(
            mail=email).first()
        if userInfo == None:
            return error(request, "Your mail is not registered to us", "Home", "/")
        otp = otpGenerate()
        GLOBAL_email = email
        GLOBAL_otp = str(otp)
        try:
            send_mail(
                "OTP | E Note Book",
                f'Hey your OTP to reset password is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except:
            return error(request, "There are some internal issue", "Home", "/")
        return render(request, "forgotOtpCheck.html")
    return render(request, "fIndex.html")


def otpcheck(request):
    global GLOBAL_match
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        userOtp = request.POST.get('otp')
        if userOtp == GLOBAL_otp:
            GLOBAL_match = True
            return render(request, "resetPassword.html")
        return error(request, "OTP not matched", "Try Again", "/forgot")
    return render(request, "forgotOtpCheck.html")


def resetPass(request):
    if request.session.get('log'):
        return redirect(homeIndex)
    if GLOBAL_match:
        if request.method == "POST":
            newPass = request.POST.get('newPass')
            newConPass = request.POST.get('newConPass')
            if newConPass == newPass:
                userInfo = UsersData.objects.filter(
                    mail=GLOBAL_email).first()
                userInfo.password = make_password(newPass)
                userInfo.save()
                return error(request, "Password reset done", "Home", "/")
            return error(request, "New password & confirm password not matched", "Try Again", "/forgot")
        return redirect(index)
    return redirect(index)
