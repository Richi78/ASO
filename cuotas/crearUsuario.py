import subprocess
import argparse

#mandar el nombre del usuario y la cuota
parser = argparse.ArgumentParser();
parser.add_argument("nombre",type=str)
def crearCuota(userName = parser.parse_args()):
    try:
        cmd = ["btrfs","subvolume","create","/srv/www/htdocs/"+userName.nombre]
#       cmd2 = ["btrfs","qgroup","limit",str(cuota)"M","/srv/www/htdocs/"+str(userName)]
        subprocess.run(cmd,check=True)
        print("usuario creado")

    except subprocess.CalledProcessError as e:
        print("error")
crearCuota()