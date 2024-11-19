#!/usr/bin/env python3
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")
from Utils.utils import whoami
from Vista.gui import Gui

if __name__ == "__main__":
    iam = whoami()
    if iam == "root": 
        print("Iniciando administrador HostingWeb")
        root = tk.Tk()
        my_gui = Gui(root)
        root.title('Proyecto ASO')
        root.mainloop()
    else: 
        messagebox.showerror(
            title="Error",
            message="Debes ejecutar la aplicacion con privilegios."
            )
        print("Ejecutar la apliacion con privilegios de administrador")