from django.shortcuts import render, redirect
from home.views import error
from home.models import NoteBook, UsersData
from notebook.views import successMessage
import json

# Create your views here.


def share(request, slug):
    if not request.session.get('log'):
        return error(request, "Login first", "Home", "/")
    notebook = NoteBook.objects.filter(slug=slug).first()
    if notebook.bookOwner != request.session.get('userName'):
        return error(request, "You are not allowed to edit this book", "Back to Home", "/")
    rawList = notebook.shareList
    userList = None
    if rawList != None:
        userList = rawList.split('"')
        for item in userList:
            if item == '':
                userList.remove(item)
    noteDict = {
        "bookName": notebook.noteName,
        "isPublic": notebook.isPublic,
        "slug": slug,
        "userList": userList,
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


def sharedList(request):
    return render(request, "sharedList.html")


def manageAccess(request, slug, targetUser, adding):
    if request.method == "POST":
        print("in fun")
        if not request.session.get('log'):
            return error(request, "Login first", "Home", "/")
        print("log check")
        getUser = UsersData.objects.filter(mail=targetUser).first()
        print(getUser)
        if getUser is None:
            return error(request, "User Not Found", "Back", "/")
        print("target check")
        getNote = NoteBook.objects.filter(slug=slug).first()
        if getNote is None:
            return error(request, "Note not found", "Back", "/")
        print("note check")
        print("all check passed")
        print(f"Note is {getNote.shareList}")
        if getNote.shareList is not None:
            getNote.shareList += json.dumps(targetUser)
        else:
            getNote.shareList = json.dumps(targetUser)
        getNote.save()
        print("last part")
    return redirect(f"/share/{slug}/")


def giveAccess(request):
    if request.method == "POST":
        if not request.session.get('log'):
            return error(request, "Login first", "Home", "/")
        targetUser = request.POST.get("targetUser")
        slug = request.POST.get("slug")
        manageAccess(request, slug, targetUser, True)
    return redirect("/")
