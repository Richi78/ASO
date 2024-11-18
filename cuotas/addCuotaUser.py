import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("nombre",type=str)
parser.add_argument("cuota",type=int)

def crearCuota(parametros = parser.parse_args()):
    try:
#        cmd = ["btrfs","subvolume","create","/srv/www/htdocs/"+str(userName)]
        cmd2 = ["btrfs","qgroup","limit",str(parametros.cuota)+"M","/srv/www/htdocs/"+parametros.nombre]
        subprocess.run(cmd2,check=True)
        print("cuota editado/creado")

    except subprocess.CalledProcessError as e:
        print("error")
crearCuota()