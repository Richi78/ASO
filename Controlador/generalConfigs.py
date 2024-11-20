import subprocess
from tkinter import messagebox
from DB.postgres import setup_postresql,setup_pg_hba
from DB.phpAdmin import installAndConfigurePhpPgAdmin,installAndConfigurePhpMyAdmin
from FTP.ftp import conf_ftp
def installApache():
    isInstalled = validateService('apache2')
    if isInstalled:
        try:
            subprocess.run(
                ['zypper','in','-y','apache2', 'apache2-mod_php7'], 
                text=True,
                capture_output=True
                )
            subprocess.run(
                ['zypper', 'in', '-y', 'php7', 'php7-mysql', 'php7-pgsql']
            )
            subprocess.run(
                ['/usr/sbin/a2enmod', 'php7']
            )
            subprocess.run(
                ['touch','/etc/apache2/.htpasswd']
            )
            subprocess.run(
                ['a2enmod', 'version']
            )
            subprocess.run(
                ["service","apache2","start"]
            )
            subprocess.run(
                ["systemctl","enable","apache2.service"]
            )
            messagebox.showinfo(
                title="Confirmacion", 
                message="El servicio Apache se ha instalado correctamente."
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

            conf_ftp()
            subprocess.run(
                ['service', 'vsftpd','start']
            )          
            messagebox.showinfo(
                title="Confirmacion", 
                message="El servicio FTP se ha instalado correctamente."
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
                ['zypper','in','-y', 'postgresql11','postgresql11-server'],
                text=True,
                capture_output=True
                )
            print("stdout: ", result.stdout)
            print("stderr: ", result.stderr)
            

            setup_postresql()
            setup_pg_hba()
            installAndConfigurePhpPgAdmin()

            #iniciar servicio
            subprocess.run(
                ["service","postgresql","start"]
            )

            messagebox.showinfo(
                title="Confirmacion", 
                message="El servicio PostgreSQL y phpPgAdmin se han instalado correctamente."
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
