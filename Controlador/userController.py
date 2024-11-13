import json
from datetime import date

def addUserToJson(name, email, domain, passwd):
    today = date.today()
    dirname = f"/srv/www/htdocs/{today.day}{today.month}{today.year}_{name}"
    user = {
        "name": name,
        "email": email,
        "domain": domain,
        "password": passwd,
        "path": dirname
        }
    with open("usersData.json", "r") as f:
        jsonData = json.load(f)
    jsonData["users"].append(user)

    with open("usersData.json", 'w') as f:
        json.dump(jsonData, f, indent=2)

    with open("usersData.json.bk", 'w') as f:
        json.dump(jsonData, f, indent=2)

def updateUser():
    pass

def deleteUser():
    pass

def listUsers():
    with open("usersData.json", "r") as f:
        data = json.load(f)
    usersList = [x["name"] for x in data["users"] ]
    return usersList