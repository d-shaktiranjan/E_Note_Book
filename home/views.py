from django.shortcuts import render, redirect, HttpResponse
from home.models import NoteBook, UsersData
from datetime import datetime
from home.randomslug import getRandomSlug
import json
import urllib.request
from home.github import profileLink

from django.contrib.auth.hashers import make_password, check_password
from home import signupFunctions
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def index(request):
    if request.session.get('log'):
        noteBooks = NoteBook.objects.filter(
            bookOwner=request.session['userName']).all()
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
                              lastDateTime=datetime.now(), dateTime=datetime.now(), slug=slug, content="", bookOwner=request.session['userName'])
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


aboutUser = {}


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        aboutUser["name"] = name
        mail = request.POST.get("mail")
        aboutUser["mail"] = mail
        password = request.POST.get("pass")
        aboutUser["pass"] = password
        cPass = request.POST.get("anotherPass")
        otp = signupFunctions.otpGenerate()
        aboutUser["otp"] = str(otp)
        if signupFunctions.checkMail(mail):
            return error(request, "Your mail is already registered to us", "Login", "/")
        if password == cPass:
            try:
                send_mail(
                    "OTP | E Note Book",
                    f'Hey your OTP is {otp}',
                    settings.EMAIL_HOST_USER,
                    [mail],
                    fail_silently=False,
                )
            except:
                return error(request, "Invalid email address", "Home", "/")
            return render(request, "otp.html")
        else:
            return error(request, "Password & confirm password not matched", "Home", "/")
    else:
        return error(request, "Not allowed", "Home", "/")


def login(request):
    if request.method == "POST":
        mail = request.POST.get("email")
        password = request.POST.get("pass")
        fetchedPass = UsersData.objects.filter(mail=mail).first()
        if fetchedPass == None:
            return error(request, "Your mail is not registered to us, Sign up first", "Home", "/")
        if check_password(password, fetchedPass.password):
            print("Yes pass macthed")
            request.session['log'] = True
            request.session['mail'] = mail
            request.session['userName'] = mail.split("@")[0]
            return redirect("index")
        else:
            return error(request, "Invalid Password", "Home", "/")
    else:
        return error(request, "Not allowed", "Home", "/")


def logout(request):
    del request.session['log']
    return redirect('index')


def otpCheck(request):
    if len(aboutUser) == 0:
        return redirect("index")
    if request.method == "POST":
        otpUser = request.POST.get("otp")
        if otpUser == aboutUser["otp"]:
            user = UsersData(mail=aboutUser["mail"], name=aboutUser["name"],
                             password=make_password(aboutUser["pass"]))
            user.save()
        else:
            print("NOT")
        return redirect("index")


def profile(request):
    if request.session.get('log'):
        return render(request, "profile.html")
    else:
        return redirect(index)


def error(request, errorMsg, buttonName, buttonLink):
    errorDict = {
        "msg": errorMsg,
        "name": buttonName,
        "link": buttonLink
    }
    return render(request, "error.html", errorDict)
