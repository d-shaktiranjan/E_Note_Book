from home.models import UsersData


def checkMail(mail):
    return bool(UsersData.objects.filter(mail=mail))
