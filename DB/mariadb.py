import subprocess

__all__ = [
    "install_mariabd",
    "enable_mariadb",
    "secure_mariadb",
    "create_database_and_user",
    "setup_mariadb"
]


def install_mariabd():
    """Instalar MariaDB si no esta instalado."""
    print("Verificando si MariaDB esta instalado...")
    if subprocess.run(["zypper", "search", "--installed-only", "mariadb-server"]):
        print("MariaDB ya esta instalado.")
    else:
        print("Instalando MariaDB...")
        if not subprocess.run(["sudo", "zypper", "refresh", "&&", "sudo", "zypper", "install", "-y", "mariadb-server"]):
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
    print("Asegurando la instalaci n de MariaDB...")

    comandos = [
        "sudo mysql -e \"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('mariadb');\"",
        "sudo mysql -e \"DELETE FROM mysql.user WHERE User='';\"",
        "sudo mysql -e \"DROP DATABASE test;\"",
        "sudo mysql -e \"DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';\"",
        "sudo mysql -e \"FLUSH PRIVILEGES;\""
    ]

    for comando in comandos:
        if not subprocess.run(comando.split(" ")):
            print("No se pudo asegurar la instalaci n de MariaDB.")
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
        print("Cambios guardados en la configuraci n de MariaDB.")

    print(f"Base de datos y usuario '{username}' creados correctamente.")
    return True

def setup_mariadb():
    """Proceso de configuracion completo para MariaDB."""
    print("Iniciando el proceso de configuraci n de MariaDB...")
    if not install_mariabd():
        return
    if not enable_mariadb():
        return
    if not secure_mariadb():
        return
    print("Configuracion de MariaDB completada correctamente.")

