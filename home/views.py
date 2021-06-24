from django.shortcuts import render, redirect, HttpResponse
from home.models import NoteBook, UsersData, SignupTempData
from datetime import datetime
from home.randomslug import getRandomSlug
import json
import urllib.request
from home.github import profileLink

from django.contrib.auth.hashers import make_password, check_password
from home import signupFunctions
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from os import mkdir, remove
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
            return redirect(index)

        if len(noteBooks) == 0:
            noteDict["nothing"] = True
        noteDict["pic"] = signupFunctions.checkPic(
            request.session.get('userName'))
        return render(request, 'index.html', noteDict)
    else:
        return render(request, "land.html")


def read(request, slug):
    note = NoteBook.objects.filter(slug=slug).first()
    if note.bookOwner != request.session.get('userName'):
        return error(request, "You are not allowed to read this book", "Back to Home", "/")
    noteDict = {
        "notes": note,
        "slug": slug,
    }
    return render(request, 'read.html', noteDict)


def delete(request, slug):
    instance = NoteBook.objects.get(slug=slug)
    if instance.bookOwner != request.session.get('userName'):
        return error(request, "You are not allowed to delete this book", "Back to Home", "/")
    instance.delete()
    response = redirect('/')
    return response


def edit(request, slug):
    note = NoteBook.objects.filter(slug=slug).first()
    if note.bookOwner != request.session.get('userName'):
        return error(request, "You are not allowed to edit this book", "Back to Home", "/")
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
    try:
        team = open("./team.json", "r")
        jsonTeam = json.loads(team.read())
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
    except:
        return error(request, "Some internal Issue", "Home", "/")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mail = request.POST.get("mail")
        password = request.POST.get("pass")
        cPass = request.POST.get("anotherPass")
        UserOtp = signupFunctions.otpGenerate()
        if signupFunctions.checkMail(mail):
            return error(request, "Your mail is already registered to us", "Login", "/")
        if password == cPass:
            try:
                send_mail(
                    "OTP | E Note Book",
                    f'Hey your OTP is {UserOtp}',
                    settings.EMAIL_HOST_USER,
                    [mail],
                    fail_silently=False,
                )
                newTemp = SignupTempData(
                    otp=UserOtp, mail=mail, name=name, password=make_password(password))
                newTemp.save()
                userDict = {"mail": mail}
            except:
                return error(request, "Invalid email address", "Home", "/")
            return render(request, "otp.html", userDict)
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
            request.session['log'] = True
            request.session['mail'] = mail
            request.session['userName'] = mail.split("@")[0]
            return redirect(index)
        else:
            return error(request, "Invalid Password", "Home", "/")
    else:
        return error(request, "Not allowed", "Home", "/")


def logout(request):
    del request.session['log']
    del request.session['mail']
    del request.session['userName']
    return redirect(index)


def otpCheck(request):
    if request.method == "POST":
        otpUser = request.POST.get("otp")
        mail = request.POST.get("mail")
        tempUser = SignupTempData.objects.filter(mail=mail).first()
        if otpUser == tempUser.otp:
            user = UsersData(mail=tempUser.mail, name=tempUser.name,
                             password=tempUser.password)
            user.save()
            tempUser.delete()
            return error(request, "Account created", "Home", "/")
        else:
            tempUser.delete()
            return error(request, "OTP not matched", "Home", "/")
        return redirect(index)


def profile(request):
    if request.session.get('log'):
        about = signupFunctions.checkPic(request.session.get('userName'))
        aboutUser = UsersData.objects.filter(
            mail=request.session.get('mail')).first()
        about["allInfo"] = aboutUser
        return render(request, "profile.html", about)
    return redirect(index)


def changeName(request):
    if request.session.get('log') and request.method == "POST":
        aboutUser = UsersData.objects.filter(
            mail=request.session.get('mail')).first()
        newName = request.POST.get('newName')
        aboutUser.name = newName
        aboutUser.save()
        return redirect(profile)
    else:
        return error(request, "Can't change the name right now", "Profile", "/profile")


def changePassword(request):
    if request.session.get('log') and request.method == "POST":
        newPass = request.POST.get('newPass')
        newConPass = request.POST.get('newConPass')
        currentPass = request.POST.get('currentPass')
        if newConPass == newPass:
            aboutUser = UsersData.objects.filter(
                mail=request.session.get('mail')).first()
            aboutUser.password = make_password(newPass)
            aboutUser.save()
            return error(request, "Password chnaged", "Profile", "/profile")
        else:
            return error(request, "Password & Confirm password not matched", "Profile", "/profile")
    else:
        return error(request, "Can't change the password right now", "Profile", "/profile")


def uploadPic(request):
    try:
        mkdir("static/userImage")
    except:
        pass
    if request.session.get('log') and request.method == "POST" and request.FILES['profilePic']:
        pic = request.FILES['profilePic']
        fs = FileSystemStorage()
        picNameList = pic.name.split(".")
        userName = request.session['userName'] + \
            "."+picNameList[len(picNameList)-1]
        userImageStatus = signupFunctions.checkPic(
            request.session.get('userName'))
        if userImageStatus["isPic"]:
            remove("static/userImage/{}".format(userImageStatus["userName"]))
        fileName = fs.save(f"static/userImage/{userName}", pic)
        uUrl = fs.url(fileName)
        return redirect(profile)
    else:
        return redirect(index)


def error(request, errorMsg, buttonName, buttonLink):
    errorDict = {
        "msg": errorMsg,
        "name": buttonName,
        "link": buttonLink
    }
    return render(request, "error.html", errorDict)
