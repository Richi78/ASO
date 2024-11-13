import json
from datetime import date
import subprocess
from Utils.utils import restartApache
import psycopg2

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

def updateUser():
    pass

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

    # conectar a la base de datos como postgres
    subprocess.run(['sudo', 'service', 'postgresql', 'start'], check=True)
    conn = psycopg2.connect(dbname="postgres", user="postgres",password="postgres")
    conn.autocommit = True
    cur = conn.cursor()

    # eliminar de base de datos con nombre del usuario si existe
    try:
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(user)))
        print(f"Base de datos '{user}' eliminada.")
    # eliminar usuario con nombre del usuario si existe
        cur.execute(sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(user)))
        print(f"Usuario '{user}' eliminado.")
    except:
        pass

    # cerrar conexion
    cur.close()
    conn.close()

    #borrar de el archivo pg_hba.conf
    hba_path = "/var/lib/pgsql/data/pg_hba.conf"
    with open(hba_path, "r") as f:
        pg_hba = f.readlines()
    index = int()
    for i in range(0,len(pg_hba)):
        if f"local   {user}" in pg_hba[i]:
            index = i
            break
    if index == 0:
        print("User not found")
    else:    
        del pg_hba[index]
        with open("/etc/postgresql/12/main/pg_hba.conf", "w") as f:
            f.writelines(pg_hba)
        print("Usuario borrado del archivo pg_hba.conf")

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
    