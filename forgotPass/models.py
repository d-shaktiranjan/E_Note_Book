from django.db import models

# Create your models here.


class ForgotTempData(models.Model):
    otp = models.CharField(max_length=10)
    mail = models.CharField(max_length=35)
