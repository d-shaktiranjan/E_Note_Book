from django.shortcuts import render
from home.models import NoteBook

# Create your views here.


def index(request):
    noteBooks = NoteBook.objects.all()
    noteDict = {
        'notes': noteBooks
    }
    return render(request, 'index.html', noteDict)
