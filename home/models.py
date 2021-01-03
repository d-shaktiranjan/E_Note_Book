from django.db import models

# Create your models here.
class NoteBook(models.Model):
    noteName = models.CharField(max_length=10)
    about = models.CharField(max_length=25)
    teachers = models.CharField(max_length=20)
    dateTime = models.DateTimeField()

    def __str__(self):
        return self.noteName