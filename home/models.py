from django.db import models
from home.utils import generateAuthKey
# Create your models here.


class NoteBook(models.Model):
    noteName = models.CharField(max_length=10)
    about = models.CharField(max_length=25)
    teachers = models.CharField(max_length=20)
    dateTime = models.DateTimeField()
    lastDateTime = models.DateTimeField()
    slug = models.CharField(max_length=25, primary_key=True)
    content = models.TextField()
    bookOwner = models.CharField(max_length=20)
    isPublic = models.BooleanField(default=False)
    shareList = models.JSONField(null=True)

    def __str__(self):
        return self.noteName


class UsersData(models.Model):
    mail = models.CharField(max_length=35)
    name = models.CharField(max_length=25)
    isTwoFactorEnabled = models.BooleanField(default=False)
    authKey = models.CharField(max_length=35, default=generateAuthKey(10))
    password = models.TextField()

    def __str__(self):
        return self.name


class SignupTempData(models.Model):
    otp = models.CharField(max_length=10)
    mail = models.CharField(max_length=35)
    name = models.CharField(max_length=25)
    password = models.TextField()
