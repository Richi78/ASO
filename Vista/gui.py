
import tkinter as tk
from tkinter import messagebox
from Controlador.generalConfigs import installApache,installFTP,installPostGreSQL
from Utils.utils import generatePassword, createDirectoryWeb

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
        
        self.userButtons = [
            {}
        ]

        self.userName = tk.StringVar(value="")
        self.passwd = tk.StringVar(value="")

        # Widgets
        
        # Frame de configuraciones generales de suse
        self.frame_generalConfigs = tk.Frame(
            self.master, 
            width=700, 
            height=200,
            pady=5
            )
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

        # Botones de instalar servicios
        for e in self.generalConfigs:
            self.createButton(
                self.frame_generalConfigs, 
                e["service"], 
                e["action"]
                )
        
        # Frame nuevo usuario
        self.frame_user = tk.Frame(
            self.master, 
            width=700, 
            height=200,
            pady=5
            )
        self.frame_user.pack()

        self.label_userLabel = tk.Label(
            self.frame_user,
            text="Nombre de usuario"
            )
        self.label_userLabel.pack(side="left")

        self.input_user = tk.Entry(
            self.frame_user,
            textvariable=self.userName
            )
        self.input_user.pack(side='left')

        self.button_generarPasswd = tk.Button(
            self.frame_user, 
            text="Generar Password",
            command=self.newPassword
            )
        self.button_generarPasswd.pack(side="left")

        self.input_password = tk.Entry(
            self.frame_user,
            textvariable=self.passwd,
            state='readonly',
            width=20
            )
        self.input_password.pack(side="left")
        
        # Frame create user
        self.frame_createUser = tk.Frame(
            self.master, 
            width=700, 
            height=200,
            pady=5
            )
        self.frame_createUser.pack()

        self.button_crearUsuario = tk.Button(
            self.frame_createUser,
            text="Crear nuevo usuario",
            command=self.createUser
        )
        self.button_crearUsuario.pack()
        
        

        # Eventos
        # self.master.bind('',)

    def createButton(self, master, text, action):
        self.button = tk.Button(master, text=text, command=action)
        self.button.pack(side='left')

    def newPassword(self):
        self.passwd.set(generatePassword())
        
    def createUser(self):
        createDirectoryWeb(self.userName.get())
        
         
        
