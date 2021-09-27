from django.shortcuts import render
from home.views import error
from home.models import NoteBook
from notebook.views import successMessage

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
        "slug": slug,
    }
    return render(request, "share.html", noteDict)


def makePublic(request):
    if request.method == "POST":
        slug = request.POST.get("slug")
        notebook = NoteBook.objects.filter(slug=slug).first()
        notebook.isPublic = True
        notebook.save()
        return successMessage(request, "Now the note is Public", "Home", "/")
    return error(request, "Not Allowed", "Home", "/")


def makePrivate(request):
    if request.method == "POST":
        slug = request.POST.get("slug")
        notebook = NoteBook.objects.filter(slug=slug).first()
        notebook.isPublic = False
        notebook.save()
        return successMessage(request, "Note is Private now", "Home", "/")
    return error(request, "Not Allowed", "Home", "/")
