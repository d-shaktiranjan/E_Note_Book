from django.shortcuts import render, redirect, HttpResponse
from home.models import NoteBook, UsersData
from datetime import datetime
from home.randomslug import getRandomSlug
import json
import urllib.request
from home.github import profileLink

from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def index(request):
    if request.session.get('log'):
        noteBooks = NoteBook.objects.all()
        noteDict = {
            'notes': noteBooks,
            'newNote': False,
        }
        if request.method == "POST":
            bName = request.POST.get('book')
            about = request.POST.get('about')
            teacher = request.POST.get('teacher')
            slug = getRandomSlug(bName, teacher)
            addNew = NoteBook(noteName=bName, about=about, teachers=teacher,
                              lastDateTime=datetime.now(), dateTime=datetime.now(), slug=slug, content="")
            addNew.save()
            noteDict.update({"newNote": True})
            noteDict["noteName"] = bName

        if len(noteBooks) == 0:
            noteDict["nothing"] = True
        return render(request, 'index.html', noteDict)
    else:
        return render(request, "land.html")


def read(request, slug):
    note = NoteBook.objects.filter(slug=slug).first()
    noteDict = {
        "notes": note,
        "slug": slug,
    }
    return render(request, 'read.html', noteDict)


def delete(request, slug):
    instance = NoteBook.objects.get(slug=slug)
    instance.delete()
    response = redirect('/')
    return response


def edit(request, slug):
    note = NoteBook.objects.filter(slug=slug).first()
    noteDict = {
        "notes": note,
        "slug": slug,
        "status": False,
    }
    if request.method == "POST":
        new = request.POST.get('newContent')
        update = NoteBook.objects.get(slug=slug)
        update.content = new
        update.lastDateTime = datetime.now()
        update.save()
        noteDict["status"] = True

    return render(request, 'edit.html', noteDict)


def team(request):
    teamPage = urllib.request.urlopen(
        'https://raw.githubusercontent.com/d-shaktiranjan/E_Note_Book/main/team.json')
    siteContent = teamPage.read()
    jsonTeam = json.loads(siteContent)
    # myDict={}
    name = []
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
    myDict = {
        "mixList": zip(name, role, github, linkdin, ig, twt, profilePic),
    }
    return render(request, 'team.html', myDict)


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        password = request.POST.get("pass")
        cPass = request.POST.get("anotherPass")
        if password == cPass:
            user = UsersData(mail=mail, name=name,
                             password=make_password(password))
            user.save()
            return redirect("index")
        else:
            return HttpResponse("<h1>Pass & C pass not macthed</h1>")
    else:
        return HttpResponse("<h1>Not allowed</h1>")


def login(request):
    if request.method == "POST":
        mail = request.POST.get("email")
        password = request.POST.get("pass")
        fetchedPass = UsersData.objects.filter(mail=mail).first()
        if check_password(password, fetchedPass.password):
            print("Yes pass macthed")
            request.session['log'] = True
            return redirect("index")
        else:
            return HttpResponse("<h1>Invalid Password or Email</h1>")
    else:
        return HttpResponse("<h1>Not allowed</h1>")
