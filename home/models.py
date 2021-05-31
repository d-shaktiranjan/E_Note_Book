from django.db import models

# Create your models here.


class NoteBook(models.Model):
    noteName = models.CharField(max_length=10)
    about = models.CharField(max_length=25)
    teachers = models.CharField(max_length=20)
    dateTime = models.DateTimeField()
    lastDateTime = models.DateTimeField()
    slug = models.CharField(max_length=25)
    content = models.TextField()
    bookOwner = models.CharField(max_length=20)

    def __str__(self):
        return self.noteName


class UsersData(models.Model):
    mail = models.CharField(max_length=35)
    name = models.CharField(max_length=25)
    password = models.TextField()

    def __str__(self):
        return self.name
