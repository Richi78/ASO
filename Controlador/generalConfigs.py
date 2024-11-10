import subprocess
from tkinter import messagebox

def installApache():
    result = subprocess.Popen(
        ['apache2-ctl', 'status'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = result.communicate()
    if result.returncode == 0:
        try:
            run_command(['zypper', 'in', '-y', 'apache2', 'apache2-mod_php7'])
            run_command(['zypper', 'in', '-y', 'php7', 'php7-mysql', 'php7-pgsql'])
            run_command(['/usr/sbin/a2enmod', 'php7'])
            run_command(['a2enmod', 'version'])
            run_command(['service', 'apache2', 'start'])
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
            result = run_command(['zypper', 'in', '-y', 'vsftpd'])
            print("stdout: ", result['stdout'])
            print("stderr: ", result['stderr'])

            # abrir puertos
            run_command(['firewall-cmd', '--permanent', '--add-port=21/tcp'])
            run_command(['firewall-cmd', '--reload'])
            print("Puerto 21 abierto")

            # iniciar servicio
            run_command(['service', 'vsftpd', 'start'])
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
            result = run_command(['zypper', 'in', '-y', 'postgresql11', 'postgresql11-server'])
            print("stdout: ", result['stdout'])
            print("stderr: ", result['stderr'])

            # iniciar servicio
            run_command(['service', 'postgresql', 'start'])
            messagebox.showinfo(
                title="Confirmacion",
                message="El servicio PostgreSQL se ha instalado correctamente."
            )
        except subprocess.CalledProcessError as e:
            print("Error al instalar PostgreSQL:", e)
    else:
        print("El servicio PostgreSQL ya esta instalado")
        messagebox.showinfo(title="Mensaje", message="El servicio PostgreSQL ya esta instalado.")

def validateService(service):
    """
    Valida si un servicio ya está instalado.
    """
    result = subprocess.Popen(
        ['service', f'{service}', 'status'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = result.communicate()
    # si stderr tiene contenido, hay que instalar
    return bool(stderr)

def run_command(cmd):
    """
    Ejecuta un comando y devuelve stdout y stderr como texto.
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return {
        'stdout': stdout.decode('utf-8'),
        'stderr': stderr.decode('utf-8'),
        'returncode': process.returncode
    }

