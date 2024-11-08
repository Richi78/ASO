import subprocess
from tkinter import messagebox

def installApache():
    isInstalled = validateService('apache2')
    if isInstalled:
        try:
            result = subprocess.run(
                ['zypper','in','-y','apache2'], 
                text=True,
                capture_output=True
                )
            print("stdout: ", result.stdout)
            print("stderr: ", result.stderr)
            subprocess.run(
                ["service","apache2","start"]
            )
        except subprocess.CalledProcessError as e:
            print("Error al instalar Apache2:", e)
    else:
        print("El servicio apache2 ya esta instalado")
        messagebox.showinfo(title="Mensaje", message="El servicio Apache ya esta instalado.")

def installFTP():
    isInstalled = validateService('vsftpd')
    if isInstalled:    
        try:
            result = subprocess.run(
                ['zypper','in','-y','vsftpd'], 
                text=True,
                capture_output=True
                )
            print("stdout: ", result.stdout)
            print("stderr: ", result.stderr)
            
            # abrir puertos
            subprocess.run(
                ['firewall-cmd', '--permanent', '--add-port=21/tcp']
            )
            subprocess.run(
                ['firewall-cmd', '--reload']
            )
            print("Puerto 21 abierto")
            # iniciar servicio
            subprocess.run(
                ['service', 'vsftpd','start']
            )            
        except subprocess.CalledProcessError as e:
            print("Error al instalar FTP:", e)
    else:
        messagebox.showinfo(title="Mensaje", message="El servicio FTP ya esta instalado.")
        print("El servicio FTP ya esta instalado")

def installPostGreSQL():
    isInstalled = validateService('postgresql')
    if isInstalled:
        try:
            result = subprocess.run(
                ['zypper','in','-y','postgresql-server'],
                text=True,
                capture_output=True
                )
            print("stdout: ", result.stdout)
            print("stderr: ", result.stderr)
            
            #iniciar servicio
            subprocess.run(
                ["service","postgresql","start"]
            )
        except subprocess.CalledProcessError as e:
            print("Error al instalar PostgreSQL:", e)
    else:
        print("El servicio PostgreSQL ya esta instalado")
        messagebox.showinfo(title="Mensaje", message="El servicio PostgreSQL ya esta instalado.")
    
def validateService(service):
    """
    Valida si un servicio ya esta instalado
    """
    result = subprocess.run(
        ['service',f'{service}','status'],
        text=True,
        capture_output=True
    )
    # si stderr tiene contenido, hay que instalar
    if result.stderr: return True
    else: return False
