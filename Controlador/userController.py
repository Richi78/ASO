import json
from datetime import date
import subprocess
from Utils.utils import restartApache
import psycopg2
from DB.postgres import delete_postgresql_database_and_user,editPassword
from DB.mariadb import delete_mariadb_database_and_user,edit_mariadb_password
from FTP.ftp import delete_ftp_user,edit_ftp_user

def addUserToJson(name, email, domain, db, diskQuote, passwd):
    today = date.today()
    dirname = f"/srv/www/htdocs/{today.day}{today.month}{today.year}_{name}"
    user = {
        "name": name,
        "email": email,
        "domain": domain,
        "password": passwd,
        "path": dirname,
        "database": db,
        "diskQuote": diskQuote
        }
    with open("usersData.json", "r") as f:
        jsonData = json.load(f)
    jsonData["users"].append(user)

    with open("usersData.json", 'w') as f:
        json.dump(jsonData, f, indent=2)

    with open("usersData.json.bk", 'w') as f:
        json.dump(jsonData, f, indent=2)

def updateUser(name, email, password, newdomain, quote, path, olddomain,db):
    #update Json
    with open("usersData.json", "r") as f:
        jsonData = json.load(f)
    usersList = jsonData["users"]
    for i in range (0, len(usersList)):
        if usersList[i]["name"] == name:
            usersList[i]["email"] = email 
            usersList[i]["password"] = password 
            usersList[i]["domain"] = newdomain 
            usersList[i]["diskQuote"] = quote
            break
    with open("usersData.json", "w") as f:
        json.dump(jsonData, f, indent=2)
    
    configFile = f"{path.split("/")[-1]}.conf"

    # update virtual host
    with open(f"/etc/apache2/vhosts.d/{configFile}", 'r') as f:
        content = f.readlines()
    
    for i in range (0,len(content)):
        if "ServerAdmin" in content[i]: content[i] = f"ServerAdmin {email}\n"
        if "ServerName" in content[i]: content[i] = f"ServerName {newdomain}\n"
    
    with open(f"/etc/apache2/vhosts.d/{configFile}", 'w') as f:
        f.writelines(content)
    
    # update hosts
    with open("/etc/hosts", "r") as f:
        hosts = f.readlines()
    
    for i in range (0,len(hosts)):
        if f"{olddomain}" in hosts[i]: 
            hosts[i] = f"127.0.0.1\t{newdomain}\n"
            break
    with open("/etc/hosts", "w") as f:
        f.writelines(hosts)
        restartApache()
    
    #update ftp
    edit_ftp_user(name, password)

    #update db
    if  db == "MariaDB":
        edit_mariadb_password(name, password)
    else:
        editPassword(name, password)
    

    restartApache()

def deleteUser(user):

    # eliminar su directorio en /srv/www/htdocs/
    subprocess.run(
        ['rm', '-r', f"{user["path"]}"]
    )

    # eliminar su virtual host en /etc/apache2/vhosts.d
    subprocess.run(
        ['rm', f"/etc/apache2/vhosts.d/{user["path"].split("/")[-1]}.conf"]
    )

    # eliminar la linea en /etc/hosts
    with open("/etc/hosts", "r") as f:
        hostsData = f.readlines()
    index = int()
    for i in range(0,len(hostsData)):
        if user["domain"] in hostsData[i]:
            index = i
            break
    del hostsData[index]

    with open("/etc/hosts", "w") as f:
        f.writelines(hostsData)

    # eliminar del json

    with open("usersData.json", "r") as f:
        data = json.load(f)
    
    for i in range(0, len(data["users"])):
        if data["users"][i]["name"] == user["name"]:
            del data["users"][i]
            break
    
    with open("usersData.json", "w") as f:
        json.dump(data, f, indent=2)

    # reiniciar apache
    restartApache()

    # eliminar el usuario del ftp
    delete_ftp_user(user["name"])

    # eliminar la base de datos
    if user["database"] == "MariaDB":
        delete_mariadb_database_and_user(user)
    elif user["database"] == "PostgreSQL":
        delete_postgresql_database_and_user(user)

   
    # return
    return {
        "status": 200,
        "message": "Se elimino usuario correctamente."
    }

def listUsers():
    with open("usersData.json", "r") as f:
        data = json.load(f)
    usersList = [x["name"] for x in data["users"] ]
    return usersList

def getUserByName(name):
    with open("usersData.json", "r") as f:
        data = json.load(f)
    for e in data["users"]:
        if e["name"] == name:
            return e
    else:
        return {}
    