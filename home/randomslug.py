from home.models import NoteBook


def checkStatus(slug):
    note = NoteBook.objects.filter(slug=slug)
    return bool(note)


def formatWord(word):
    new = word.replace(" ", "")
    chars = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    final = ""
    for char in new:
        if char not in chars:
            final += char
    return final


def getRandomSlug(bookName, teacher):
    getMix = formatWord(bookName.lower()) + "by" + formatWord(teacher.lower())
    if checkStatus(getMix):
        for i in range(1, 50):
            getMix = getMix + str(i)
            if not(checkStatus(getMix)):
                return getMix
    else:
        return getMix
