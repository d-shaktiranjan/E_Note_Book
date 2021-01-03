from home.models import NoteBook

def checkStatus(slug):
    note = NoteBook.objects.filter(slug = slug)
    return bool(note)

def removeSpace(word):
    return word.replace(" ","")

def getRandomSlug(bookName, teacher):
    getMix = removeSpace(bookName.lower()) + "by" + removeSpace(teacher.lower())
    if checkStatus(getMix):
        for i in range(1, 50):
            getMix = getMix + str(i)
            if not(checkStatus(getMix)):
                return getMix
    else:
        return getMix
    