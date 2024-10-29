#!/usr/bin/env python3
import tkinter as tk
from Utils.utils import whoami
from Vista.gui import Gui

if __name__ == "__main__":
    iam = whoami()
    if iam == "root": 
        print("Tas bien :D jaja, aqui viene la interfaz que esta en desarrollo")
        my_gui = Gui()
    else: print("Ejecutar la apliacion con privilegios de administrador")