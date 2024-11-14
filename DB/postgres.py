import subprocess
import psycopg2
from psycopg2 import sql


# Verificar que postgres no este instalado
__all__ = [
    "check_postgresql_installed",
    "install_services",
    "configure_postgresql",
    "configure_pg_hba",
    "create_home_directory",
    "connect_to_db",
    "delete_postgresql_database_and_user",
]


def check_postgresql_installed():
    try:
        # Ejecuta el comando para obtener la versión de PostgreSQL
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True, check=True)
        print("PostgreSQL ya está instalado:", result.stdout)
        return True
    except subprocess.CalledProcessError:
        print("PostgreSQL no está instalado.")
        return False

#Función para instalar PostgreSQL y Apache
def install_services():
    try:
        # Instalar PostgreSQL y Apache
        subprocess.run(['sudo', 'zypper', 'refresh'], check=True)
        subprocess.run(['sudo', 'zypper', 'install', 'postgresql-server', 'postgresql'], check=True)
        subprocess.run(['sudo', 'service', 'postgresql', 'start'], check=True)

        print("PostgreSQL instalado.")
    except subprocess.CalledProcessError as e:
        print("Error en la instalación: ", e)

# 2. Crear base de datos y usuario en PostgreSQL
def configure_postgresql(db_name, db_user, db_password):
    try:
        # Conectar a PostgreSQL como el usuario postgres
        subprocess.run(['sudo', 'service', 'postgresql', 'start'], check=True)
        conn = psycopg2.connect(dbname="postgres", user="postgres",password="postgres")
        conn.autocommit = True
        cur = conn.cursor()

        # Crear base de datos y usuario con permisos limitados
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        cur.execute(sql.SQL("CREATE USER {} WITH ENCRYPTED PASSWORD %s").format(sql.Identifier(db_user)), [db_password])
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(sql.Identifier(db_name), sql.Identifier(db_user)))

        # Restricciones de acceso a otras bases de datos
        cur.execute(sql.SQL("REVOKE CONNECT ON DATABASE postgres FROM {}").format(sql.Identifier(db_user)))
        print(f"Base de datos '{db_name}' y usuario '{db_user}' configurados con acceso restringido.")

        # Cerrar conexión
        cur.close()
        conn.close()
    except Exception as e:
        print("Error en la configuración de PostgreSQL: ", e)

# 3. Configurar archivo pg_hba.conf para limitar el acceso local
def configure_pg_hba(db_name, db_user):
    try:
        hba_path = "/var/lib/pgsql/data/pg_hba.conf"
        # Configuración de acceso local
        lines = []
        # Abrir el archivo pg_hba.conf
        with open(hba_path, "r") as hba_file:
            lines = hba_file.readlines()
        # Configurar la linea a insertarce en la configuracion
        new_line = f"{'local':<8}{db_user:<16}{db_name:<40}{'md5':<}"
        # Insertar la nueva linea
        lines[83] = new_line + "\n" + lines[83]
        # Guardar la configuracion
        with open(hba_path, "w") as hba_file:
            hba_file.writelines(lines)
        # Reiniciar el servicio postgresql
        subprocess.run(['sudo', 'service','postgresql', 'restart'], check=True)
        print("Archivo pg_hba.conf configurado y PostgreSQL reiniciado.")
    except Exception as e:
        print("Error al configurar pg_hba.conf: ", e)

def create_home_directory(username):
    # Define the path for the user's home directory
    home_directory = f"/home/{username}"
    
    # Check if the directory already exists
    if not os.path.exists(home_directory):
        try:
            # Create the directory
            os.makedirs(home_directory)
            print(f"Directory {home_directory} created.")
            
            # Set ownership of the directory to the user
            # subprocess.run(['sudo', 'chown', f'{username}:{username}', home_directory], check=True)
            # print(f"Ownership of {home_directory} set to {username}.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Directory {home_directory} already exists.")

def connect_to_db(db_name, db_user, db_password):
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password)
        print("Connected to the database.")
        return conn
    except Exception as e:
        print("Error connecting to the database: ", e)

def delete_postgresql_database_and_user(username):
    try:
        conn = connect_to_db("postgres", "postgres", "postgres")
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {username};")
        cur.execute(f"DROP USER IF EXISTS '{username}'@'localhost';")
        cur.close() 
        conn.close()
        print("Database and user deleted successfully.")
    except Exception as e:
        print("Error deleting database and user: ", e)
    delete_from_pg_hba(username)


def delete_from_pg_hba(db_user):
    hba_path = "/var/lib/pgsql/data/pg_hba.conf"
    with open(hba_path, "r") as f:
        pg_hba = f.readlines()
    index = int()
    for i in range(0,len(pg_hba)):
        if f"local   {db_user}" in pg_hba[i]:
            index = i
            break
    if index == 0:
        print("User not found")
    else:    
        del pg_hba[index]
        with open("/var/lib/pgsql/data/pg_hba.conf", "w") as f:
            f.writelines(pg_hba)
        print("Usuario borrado del archivo pg_hba.conf")
