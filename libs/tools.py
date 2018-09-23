def buildTemp(user):
    temp={}
    for key in user:
        if "temp." in key:
            temp[key.split('.')[1]]=user[key]
    return temp