import subprocess
import tkinter as tk
from tkinter import messagebox

def establecerCuota(usuario, block_suave, block_duro, inode_suave, inode_duro,sistema_de_archivos="/"):
    try:
        subprocess.run([
            "edquota","-u",str(usuario),str(block_suave),
            str(inode_suave),str(inode_duro),
            sistema_de_archivos
        ], check=True)
        messagebox(
            title = "",
            message = "La cuota a sido creada exitosamente"
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror(
            title = "Error",
            message="Algo salio mal"
        )
