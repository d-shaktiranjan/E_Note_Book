from django.shortcuts import render, redirect
from home.views import index, error
from home.models import UsersData

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
    return render(request, "fIndex.html")
