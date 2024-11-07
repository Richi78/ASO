import subprocess
import string
import random
from datetime import date

def whoami() -> str:
    iam = subprocess.run(['whoami'], capture_output=True, text=True)
    return iam.stdout.strip()

def generatePassword() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(32))
    return password

def crearIndex(name):
    today = date.today()
    dirname = str(today.day)+str(today.month)+str(today.year)+f"_{name}"
    subprocess.run(
        ['mkdir', f'/srv/www/htdocs/{dirname}']
    )
    subprocess.run(
        ['touch',f'/srv/www/htdocs/{dirname}/index.html']
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
        
        