from django.shortcuts import render, redirect
from home.views import index, error
from home.models import UsersData
from django.core.mail import send_mail
from django.conf import settings
from home.signupFunctions import otpGenerate

# Create your views here.


def index(request):
    if request.session.get('log'):
        return redirect(index)
    if request.method == "POST":
        email = request.POST.get('email')
        userInfo = UsersData.objects.filter(
            mail=email).first()
        if userInfo == None:
            return error(request, "Your mail is not registered to us", "Home", "/")
        otp = otpGenerate()
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
    return render(request, "fIndex.html")
