from datetime import date
import subprocess


__all__ = ['conf_ftp', 'add_ftp_user']

def conf_ftp():
    vsftpdFile = '/etc/vsftpd.conf'

    try:
        # Leer el archivo línea por línea
        with open(vsftpdFile, "r") as f:
            vsftpd = f.readlines()

        # Buscar la línea de referencia y realizar los reemplazos
        index_local_enable = -1
        index_umask = -1
        index_write_enable = -1
        index_chroot_local_user = -1
        index_chroot_list_enable = -1
        index_chroot_list_enable_2 = -1
        index_chroot_list_file = -1
        index_allow_writeable_enable = -1
        for i in range(len(vsftpd)):
            if "write_enable=NO" in vsftpd[i]:
                index_write_enable = i
            if "local_umask=022" in vsftpd[i]:
                index_umask = i
            if "local_enable=NO" in vsftpd[i]:
                index_local_enable = i
            if "#chroot_local_user=YES" in vsftpd[i]:
                index_chroot_local_user = i
            if "#chroot_list_enable=YES" in vsftpd[i]:
                index_chroot_list_enable = i
            if "chroot_list_enable=YES" in vsftpd[i]:
                index_chroot_list_enable_2 = i
            if "allow_writeable_chroot=YES" in vsftpd[i]:
                index_allow_writeable_enable = i
            if "#chroot_list_file=/etc/vsftpd.chroot_list" in vsftpd[i]:
                index_chroot_list_file = i

        if index_local_enable == -1:
            print("Línea no encontrada.")


        # Reemplazar las líneas después de la línea encontrada
        if index_local_enable != -1:
            vsftpd[index_local_enable] = "local_enable=YES\n"
        if index_write_enable != -1:
            vsftpd[index_write_enable] = "write_enable=YES\n"
        if index_umask != -1:
            vsftpd[index_umask] = "local_umask=022\n"
        if index_chroot_local_user != -1:
            vsftpd[index_chroot_local_user] = "chroot_local_user=YES\n"
        if index_chroot_list_enable != -1:
            vsftpd[index_chroot_list_enable] = "chroot_list_enable=YES\n"
            if index_allow_writeable_enable == -1:
                vsftpd[index_chroot_list_enable] = vsftpd[index_chroot_list_enable] + "allow_writeable_chroot=YES\n"
        elif index_chroot_list_enable_2 != -1:
            if index_allow_writeable_enable == -1:
                vsftpd[index_chroot_list_enable_2] = vsftpd[index_chroot_list_enable_2] + "allow_writeable_chroot=YES\n"
        
        if index_chroot_list_file != -1:
            vsftpd[index_chroot_list_file] = "chroot_list_file=/etc/vsftpd.chroot_list\n"

        # Escribir los cambios en el archivo
        with open(vsftpdFile, "w") as f:
            f.writelines(vsftpd)

        print("Líneas reemplazadas correctamente en el archivo vsftpd.conf.")

        # Crear el archivo vsftpd.chroot_list
        with open("/etc/vsftpd.chroot_list", "w") as f:
            f.write("root\n")

        subprocess.run(['service', 'vsftpd', 'restart'], check=True)

        print("archivo /etc/vsftpd.chroot_list creada y Servicio vsftpd reiniciado.")

    except FileNotFoundError:
        print(f"Archivo no encontrado: {vsftpdFile}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def add_ftp_user(username, password):
    today = date.today()
    #Agregar usuario
    dirname = f"/srv/www/htdocs/{today.day}{today.month}{today.year}_{username}"
    subprocess.run(['useradd', '-d', f'{dirname}', '-M', username], check=True)
    subprocess.run(['passwd', username], input=f"{password}\n{password}\n", text=True, check=True)
    #Quitar acceso por shell
    subprocess.run(
        ['sudo', 'chown', '-R', f'{username}:users', dirname]
    )
    subprocess.run(
        ['sudo', 'chmod', '-R', '755', dirname]
    )
    subprocess.run(['sudo', 'usermod', '-s', '/bin/false', username])
    subprocess.run(['service','vsftpd','restart'], check=True)



def delete_ftp_user(username):
    subprocess.run(['userdel', username], check=True)

    with open('/etc/vsftpd.chroot_list', 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == username:
            del lines[i]
            break

    with open('/etc/vsftpd.chroot_list', 'w') as f:
        f.writelines(lines)
    subprocess.run(['service','vsftpd','restart'], check=True)



def edit_ftp_user(username, new_password):
    subprocess.run(['passwd', username], input=f"{new_password}\n{new_password}\n", text=True, check=True)
    subprocess.run(['service','vsftpd','restart'], check=True)
