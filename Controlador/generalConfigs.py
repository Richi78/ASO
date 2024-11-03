import subprocess

def installApache():
    try:
        result = subprocess.run(
            ['zypper','in','-y','apache2'], 
            check=True, 
            text=True,
            capture_output=True
            )
        print("stdout: ", result.stdout)
        print("stderr: ", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error al instalar Apache2:", e)

def installFTP():
    try:
        result = subprocess.run(
            ['zypper','in','-y','vsftpd'], 
            check=True, 
            text=True,
            capture_output=True
            )
        print("stdout: ", result.stdout)
        print("stderr: ", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error al instalar FTP:", e)

def installPostGreSQL():
    try:
        result = subprocess.run(
            ['zypper','in','-y','postgresql11'], 
            check=True, 
            text=True,
            capture_output=True
            )
        print("stdout: ", result.stdout)
        print("stderr: ", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error al instalar PostgreSQL:", e)

def validateService(service):
    pass