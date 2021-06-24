from django.shortcuts import render, HttpResponse
from home.views import error
from home.models import NoteBook

# Create your views here.


def share(request, slug):
    if not request.session.get('log'):
        return error(request, "Login first", "Home", "/")
    notebook = NoteBook.objects.filter(slug=slug).first()
    if notebook.bookOwner != request.session.get('userName'):
        return error(request, "You are not allowed to edit this book", "Back to Home", "/")
    noteDict = {
        "bookName": notebook.noteName,
        "isPublic": notebook.isPublic,
    }
    return render(request, "share.html", noteDict)


def makePublic(request):
    return HttpResponse("URL TEST")
