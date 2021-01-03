from django.shortcuts import render
from home.models import NoteBook
from datetime import datetime
from home.randomslug import getRandomSlug
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
        slug = getRandomSlug(bName, teacher)
        addNew = NoteBook(noteName = bName, about = about, teachers = teacher, dateTime = datetime.now(), slug = slug, content = "")
        addNew.save()

    return render(request, 'index.html', noteDict)
