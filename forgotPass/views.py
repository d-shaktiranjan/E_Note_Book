from django.shortcuts import render, redirect, HttpResponse
from home.views import index as homeIndex, error
from home.models import UsersData
from django.core.mail import send_mail
from django.conf import settings
from home.signupFunctions import otpGenerate

# Create your views here.

userDict = {}


def index(request):
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        email = request.POST.get('email')
        userInfo = UsersData.objects.filter(
            mail=email).first()
        if userInfo == None:
            return error(request, "Your mail is not registered to us", "Home", "/")
        otp = otpGenerate()
        userDict["otp"] = str(otp)
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
    if request.session.get('log'):
        return redirect(homeIndex)
    if request.method == "POST":
        userOtp = request.POST.get('otp')
        if userOtp == userDict["otp"]:
            return error(request, "Otp match", "Btn", "/forgot")
        return error(request, "Otp not match", "Btn", "/forgot")
    return render(request, "forgotOtpCheck.html")
