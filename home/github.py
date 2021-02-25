def getUserName(urlList):
    myList = []
    for item in urlList:
        myUrl = str(item)
        wordList = myUrl.split("/")
        userName = wordList[3]
        myList.append(userName)
    return myList


def profileLink(userList):
    myList = []
    base = "https://avatars.githubusercontent.com/"
    newList = getUserName(userList)
    for item in newList:
        fullUrl = base+item
        myList.append(fullUrl)
    return myList
