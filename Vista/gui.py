
import tkinter as tk
from Controlador.generalConfigs import installApache,installFTP,installPostGreSQL

class Gui:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry('700x500')

        # Color
        # self.color= tk.StringVar()

        # Otros
        self.generalConfigs = [
            {"service": "Apache", "action": installApache},
            {"service": "FTP", "action": installFTP}, 
            {"service": "PostgreSQL", "action": installPostGreSQL}
            ]

        # Widgets
        
        # Frame de configuraciones generales de suse
        self.frame_generalConfigs = tk.Frame(self.master, width=700, height=200)
        self.frame_generalConfigs.pack()
        # self.frame_generalConfigs.config(bg="lightblue")

        # Label 
        self.label_generalConfigs = tk.Label(
            self.frame_generalConfigs, 
            text="Instalar servicios",
            padx=20,
            pady=5
            )
        self.label_generalConfigs.pack(side="left")

        # Botones
        for e in self.generalConfigs:
            self.createButton(
                self.frame_generalConfigs, 
                e["service"], 
                e["action"]
                )


        # Eventos
        # self.master.bind('',)

    def createButton(self, master, text, action):
        self.button = tk.Button(master, text=text, command=action)
        self.button.pack(side='left')
