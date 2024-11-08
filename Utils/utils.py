import subprocess
import string
import random
from datetime import date
from tkinter import messagebox

def whoami() -> str:
    iam = subprocess.run(['whoami'], capture_output=True, text=True)
    return iam.stdout.strip()

def generatePassword() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(16))
    return password

def createDirectoryWeb(name):
    today = date.today()
    dirname = str(today.day)+str(today.month)+str(today.year)+f"_{name}"
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
        
def verifyUser(name):
    users = subprocess.run(
        ['ls', '/srv/www/htdocs/'],
        text=True,
        capture_output=True
    )
    usersList = users.stdout.split()[:-1]
    usersList = list(map(lambda x: x.split('_')[1], usersList))
    if name in usersList: 
        return {"status": 400, "message": "Este nombre de usuario ya existe"}
    return {"status": 200, "message": "El nombre de usuario esta disponible"}
        
