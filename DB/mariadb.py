import subprocess
from tkinter import messagebox
from DB.phpAdmin import installAndConfigurePhpMyAdmin
__all__ = [
    "install_mariabd",
    "enable_mariadb",
    "secure_mariadb",
    "create_database_and_user",
    "delete_mariadb_database_and_user",
    "setup_mariadb",
    "edit_mariadb_password"
]




def install_mariabd():
    """Instalar MariaDB si no esta instalado."""
    print("Verificando si MariaDB esta instalado...")
    if subprocess.run(["zypper", "search", "--installed-only", "mariadb-server"]):
        print("MariaDB ya esta instalado.")
    else:
        print("Instalando MariaDB...")
        if not subprocess.run(["zypper", "install", "-y", "mariadb-server"]):
            print("No se pudo instalar MariaDB.")
            return False
        print("MariaDB instalado correctamente.")
    return True

def enable_mariadb():
    """Habilitar e iniciar el servicio de MariaDB."""
    print("Habilitando y iniciando el servicio MariaDB...")
    return subprocess.run(["sudo", "systemctl", "enable", "--now", "mariadb"])

def secure_mariadb():
    """Ejecutar la configuracion de mysql_secure_installation."""
    print("Asegurando la instalaci0n de MariaDB...")

    comandos = [
        f"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('mariadb');",
        f"DELETE FROM mysql.user WHERE User='';",
        f"DROP DATABASE IF EXISTS test;",
        f"DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';",
        f"FLUSH PRIVILEGES;"
    ]

    for comando in comandos:
        if not subprocess.run(["sudo","mysql", "-e", comando]):
            print("No se pudo asegurar la instalacion de MariaDB.")
            return False
    print("MariaDB asegurado correctamente.")
    
    return True

def create_database_and_user(username, password):
    """Crear una nueva base de datos y usuario con privilegios solo en esa base de datos."""
    print(f"Creando base de datos y usuario para '{username}'...")

    # Crear la base de datos para el usuario
    if subprocess.run(["sudo", "mysql", "-e", f"CREATE DATABASE {username};"]):
        print(f"Base de datos '{username}' creada.")
    else:
        print(f"Error al crear la base de datos '{username}'.")
        return False
    if subprocess.run(["sudo", "mysql", "-e", f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';"]):
        print(f"Usuario '{username}' creado.")
    else:
        print(f"Error al crear el usuario '{username}'.")
        return False
    if subprocess.run(["sudo", "mysql", "-e", f"GRANT ALL PRIVILEGES ON {username}.* TO '{username}'@'localhost';"]):
        print(f"Permisos asignados al usuario '{username}' sobre '{username}'.")
    else:
        print(f"Error al asignar permisos al usuario '{username}' sobre '{username}'.")
        return False
    if subprocess.run(["sudo", "mysql", "-e", "FLUSH PRIVILEGES;"]):
        print("Cambios guardados en la configuracion de MariaDB.")

    print(f"Base de datos y usuario '{username}' creados correctamente.")
    return True

def delete_mariadb_database_and_user(username):
    """Eliminar la base de datos y usuario creados anteriormente."""
    print(f"Eliminando base de datos y usuario para '{username}'...")

    if subprocess.run(["sudo", "mysql", "-e", f"DROP DATABASE IF EXISTS {username};"]):
        print(f"Base de datos '{username}' eliminada.")
    else:
        print(f"Error al eliminar la base de datos '{username}'.")
        return False
    if subprocess.run(["sudo", "mysql", "-e", f"DROP USER IF EXISTS '{username}'@'localhost';"]):
        print(f"Usuario '{username}' eliminado.")
    else:
        print(f"Error al eliminar el usuario '{username}'.")
        return False
    if subprocess.run(["sudo", "mysql", "-e", "FLUSH PRIVILEGES;"]):
        print("Cambios guardados en la configuracion de MariaDB.")

    print(f"Base de datos y usuario '{username}' eliminados correctamente.")
    return True

def setup_mariadb():
    """Proceso de configuracion completo para MariaDB."""
    isInstalled = isPhpMyAdminInstalled() 
    if "phpMyAdmin" in isInstalled:
        messagebox.showinfo(
                title="Mensaje", 
                message="El servicio MariaDB y PHPMyAdmin ya estan instalados."
                )
        return

    print("Iniciando el proceso de configuracion de MariaDB...")
    install_mariabd()
    enable_mariadb()
    secure_mariadb()
    installAndConfigurePhpMyAdmin()
  
    print("Configuracion de MariaDB completada correctamente.")
    messagebox.showinfo(
                title="Confirmacion", 
                message="El servicio MariaDB y PHPMyAdmin se han instalado correctamente."
                )


def edit_mariadb_password(username, new_password):
    print(f"Editando la contraseña del usuario '{username}' en MariaDB...")
    if subprocess.run(["sudo", "mysql", "-e", f"ALTER USER '{username}'@'localhost' IDENTIFIED BY '{new_password}';"]):
        print(f"Contraseña del usuario '{username}' editada correctamente.")
    else:
        print(f"Error al editar la contraseña del usuario '{username}'.")
    
def isPhpMyAdminInstalled():
    result = subprocess.run(
        ["rpm -qa | grep phpMyAdmin"],
        shell=True,
        text=True,
        capture_output=True
    )
    return result.stdout
