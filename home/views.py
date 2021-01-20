from django.shortcuts import render, redirect
from home.models import NoteBook
from datetime import datetime
from home.randomslug import getRandomSlug
# Create your views here.


def index(request):
    noteBooks = NoteBook.objects.all()
    noteDict = {
        'notes': noteBooks,
        'newNote' : False,
    }
    if request.method == "POST":
        bName = request.POST.get('book')
        about = request.POST.get('about')
        teacher = request.POST.get('teacher')
        slug = getRandomSlug(bName, teacher)
        addNew = NoteBook(noteName = bName, about = about, teachers = teacher,
         lastDateTime = datetime.now(), dateTime = datetime.now(), slug = slug, content = "")
        addNew.save()
        noteDict.update({"newNote" : True})
        noteDict["noteName"] = bName

    return render(request, 'index.html', noteDict)

def read(request, slug):
    note = NoteBook.objects.filter(slug = slug).first()
    noteDict = {
        "notes" : note,
        "slug" : slug,
        }
    return render(request,'read.html',noteDict)

def delete(request, slug):
    instance = NoteBook.objects.get(slug = slug)
    instance.delete()
    response = redirect('/')
    return response

def edit(request, slug):
    note = NoteBook.objects.filter(slug = slug).first()
    noteDict = {
        "notes" : note,
        "slug" : slug,
        "status" : False,
        }
    if request.method == "POST":
        new = request.POST.get('newContent')
        update = NoteBook.objects.get(slug = slug)
        update.content = new
        update.lastDateTime = datetime.now()
        update.save()
        noteDict["status"] = True

    return render(request,'edit.html',noteDict)