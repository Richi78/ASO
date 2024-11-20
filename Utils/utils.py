import subprocess
import string
import random
from datetime import date
from tkinter import messagebox
import json


def whoami() -> str:
    iam = subprocess.run(['whoami'], capture_output=True, text=True)
    return iam.stdout.strip()

def generatePassword() -> str:
    specialChar = "@/?|[]!)()="
    characters = string.ascii_letters + string.digits + specialChar
    password = ''.join(random.choice(characters) for _ in range(16))
    return password

def createDirectoryWeb(name):
    today = date.today()
    # dirname = str(today.day)+str(today.month)+str(today.year)+
    dirname = f"{today.day}{today.month}{today.year}_{name}"
    subprocess.run(
        ['mkdir', f'/srv/www/htdocs/{dirname}']
    )
    
    subprocess.run(
        ['touch',f'/srv/www/htdocs/{dirname}/index.html']
    )
    subprocess.run(
        ['touch',f'/srv/www/htdocs/{dirname}/phpinfo.php']
    )
    with open(f"/srv/www/htdocs/{dirname}/index.html", 'w') as f:
        f.write("<!DOCTYPE html>")
        f.write('<html lang="en">')
        f.write("<head>")
        f.write(f"<title>Sitio de {name} </title>")
        f.write("</head>")
        f.write("<body>")
        f.write(f"<h1>Este es el sitio de {name} </h1>")
        f.write("</body>")
        f.write("</html>")
    with open(f"/srv/www/htdocs/{dirname}/phpinfo.php", 'w') as f:
        f.write("<?php phpinfo(); ?>")

def createVirtualHost(name, email, domain):
    today = date.today()
    # dirname = str(today.day)+str(today.month)+str(today.year)+
    dirname = f"{today.day}{today.month}{today.year}_{name}"
    subprocess.run(
        ['touch',f'/etc/apache2/vhosts.d/{dirname}.conf']
    )
    with open(f"/etc/apache2/vhosts.d/{dirname}.conf", "w") as f:
        f.write("<VirtualHost *:80>\n")
        f.write(f"ServerAdmin {email}\n")
        f.write(f"ServerName {domain}\n")
        f.write(f"DocumentRoot /srv/www/htdocs/{dirname}\n")
        f.write("HostnameLookups Off\n")
        f.write("UseCanonicalName Off\n")
        f.write("ServerSignature On\n")
        f.write(f"<Directory '/srv/www/htdocs/{dirname}'>\n")
        f.write("AllowOverride All\n")
        f.write("Require all granted\n")
        f.write("</Directory>\n")
        f.write("</VirtualHost>\n")

    
        
def verifyUser(name, email, domain, passwd, db, quote):
    if name == "" : return {"status": 400, "message": "El nombre de usuario es obligatorio."}
    if email == "" : return {"status": 400, "message": "El correo electronico del usuario es obligatorio."}
    if domain == "" : return {"status": 400, "message": "El nombre de dominio es obligatorio."}
    if passwd == "" : return {"status": 400, "message": "El password es obligatorio."}
    if db == "" : return {"status": 400, "message": "El tipo de base de datos es obligatorio."}
    if quote == "" : return {"status": 400, "message": "El quota de disco es obligatorio."}
    with open("usersData.json", "r", encoding='utf-8') as f:
        jsonData = json.load(f)
    usersList = [x["name"] for x in jsonData["users"] ]
    if name in usersList: 
        return {"status": 400, "message": "Este nombre de usuario ya existe"}
    return {"status": 200, "message": "El nombre de usuario esta disponible"}
        
def restartApache():
    subprocess.run(
        ['service','apache2','restart']
    )

def modifyHosts(domain):
    with open('/etc/hosts', 'a') as f:
        f.write(f"127.0.0.1\t{domain}\n")