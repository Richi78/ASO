#!/usr/bin/env python3
try:
    import tkinter as tk
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")
from Utils.utils import whoami
from Vista.gui import Gui

if __name__ == "__main__":
    iam = whoami()
    if iam == "root": 
        print("Tas bien :D jaja, aqui viene la interfaz que esta en desarrollo")
        root = tk.Tk()
        my_gui = Gui(root)
        root.title('Proyecto ASO')
        root.mainloop()
    else: print("Ejecutar la apliacion con privilegios de administrador")