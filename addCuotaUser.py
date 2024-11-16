import subprocess

#para formato ext4
#pasar como parametros:
#nombre del usuario y la cuota de disco en KB
def addQuota(userName,QuotaKB):
    try:
        cmd = ["setquota",str(userName),"0",str(QuotaKB),"0","0","/mnt/lvm01"]
        subprocess.run(cmd, check=True)
        print("Configurado")

    except subprocess.CalledProcessError as e:
        print ("error")
