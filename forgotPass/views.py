from django.shortcuts import render, redirect
from home.views import index

# Create your views here.


def index(request):
    if (request.session.get('log')):
        return redirect(index)
    return render(request, "fIndex.html")
