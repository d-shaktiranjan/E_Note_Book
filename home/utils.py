import secrets
import string
import random


# generate random auth secret token
def generateAuthKey(length):
    res = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=length))
    return res
