import subprocess

#mandar el nombre de usuario y la cuota
def activarCuota():
    try:
        cmd = ["btrfs","quota","enable","/srv"]
        subprocess.run(cmd, check=True)
        print("activada")
    except subprocess.CalledProcessError as e:
        print("error",e)
activarCuota()