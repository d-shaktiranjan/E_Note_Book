from django.shortcuts import render
from home.models import NoteBook
from datetime import datetime

# Create your views here.


def index(request):
    noteBooks = NoteBook.objects.all()
    noteDict = {
        'notes': noteBooks
    }
    if request.method == "POST":
        bName = request.POST.get('book')
        about = request.POST.get('about')
        teacher = request.POST.get('teacher')
        addNew = NoteBook(noteName = bName, about = about, teachers = teacher, dateTime = datetime.now())
        addNew.save()

    return render(request, 'index.html', noteDict)
