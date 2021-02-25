from django.shortcuts import render, redirect
from home.models import NoteBook
from datetime import datetime
from home.randomslug import getRandomSlug
import json
import urllib.request
from home.github import profileLink
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

def team(request):
    teamPage = urllib.request.urlopen('https://raw.githubusercontent.com/d-shaktiranjan/E_Note_Book/main/team.json')
    siteContent = teamPage.read()
    jsonTeam = json.loads(siteContent)
    # myDict={}
    name =[]
    role = []
    github = []
    linkdin = []
    ig = []
    twt = []
    
    for i in range(len(jsonTeam)):
        name.append(jsonTeam[i]['name'])
        role.append(jsonTeam[i]['role'])
        github.append(jsonTeam[i]['github'])
        linkdin.append(jsonTeam[i]['linkdin'])
        ig.append(jsonTeam[i]['ig'])
        twt.append(jsonTeam[i]['twt'])

    profilePic = profileLink(github)
    myDict={
        "mixList":zip(name,role,github,linkdin,ig,twt,profilePic),
    }
    return render(request,'team.html',myDict)