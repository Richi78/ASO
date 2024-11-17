import subprocess

#mandar el nombre del usuario y la cuota
def crearCuota(userName):
    try:
        cmd = ["btrfs","subvolume","create","/srv/www/htdocs/"+userName]
#       cmd2 = ["btrfs","qgroup","limit",str(cuota)"M","/srv/www/htdocs/"+str(userName)]
        subprocess.run(cmd,check=True)
        print("subvolumen creado")

    except subprocess.CalledProcessError as e:
        print("error")
crearCuota()