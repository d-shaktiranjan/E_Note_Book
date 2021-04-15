from home.models import UsersData
from random import randint


def checkMail(mail):
    return bool(UsersData.objects.filter(mail=mail))


def otpGenerate():
    range_start = 10**(6-1)
    range_end = (10**6)-1
    return randint(range_start, range_end)
