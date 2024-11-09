
import tkinter as tk
from tkinter import messagebox
from Controlador.generalConfigs import installApache,installFTP,installPostGreSQL
from Utils.utils import generatePassword, createDirectoryWeb, verifyUser, createVirtualHost, restartApache, modifyHosts

class Gui:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry('600x300')

        # Otros
        self.generalConfigs = [
            {"service": "Apache+PHP7", "action": installApache},
            {"service": "FTP", "action": installFTP}, 
            {"service": "PostgreSQL", "action": installPostGreSQL}
            ]
        
        self.userButtons = [
            {}
        ]

        self.userName = tk.StringVar(value="")
        self.userEmail = tk.StringVar(value="")
        self.userDomain = tk.StringVar(value="")
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
            height=20,
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
        self.input_user.pack(side="left")

        # Frame email

        self.frame_email = tk.Frame(
            self.master, 
            width=700, 
            height=20,
            pady=5
            )
        self.frame_email.pack()

        self.label_emailLabel = tk.Label(
            self.frame_email,
            text="Correo electronico"
            )
        self.label_emailLabel.pack(side="left")

        self.input_email = tk.Entry(
            self.frame_email,
            textvariable=self.userEmail
            )
        self.input_email.pack(side="left")

        # Frame domain

        self.frame_domain = tk.Frame(
            self.master, 
            width=700, 
            height=20,
            pady=5
            )
        self.frame_domain.pack()

        self.label_domainLabel = tk.Label(
            self.frame_domain,
            text="Nombre de dominio"
            )
        self.label_domainLabel.pack(side="left")

        self.input_domain = tk.Entry(
            self.frame_domain,
            textvariable=self.userDomain
            )
        self.input_domain.pack(side="left")

        # Frame password

        self.frame_passwd = tk.Frame(
            self.master, 
            width=700, 
            height=20,
            pady=5
            )
        self.frame_passwd.pack()

        self.button_generarPasswd = tk.Button(
            self.frame_passwd, 
            text="Generar Password",
            command=self.newPassword
            )
        self.button_generarPasswd.pack(side="left")

        self.input_password = tk.Entry(
            self.frame_passwd,
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
        name = self.userName.get()
        email = self.userEmail.get()
        domain = self.userDomain.get()
        passwd = self.passwd.get()
        status = verifyUser(name=name, email=email, domain=domain, passwd=passwd)
        if status["status"] == 400:
            messagebox.showerror(
                title="Error",
                message=status["message"]
            )
            return
        createDirectoryWeb(name)
        createVirtualHost(name=name, email=email, domain=domain)
        modifyHosts(domain=domain)
        restartApache()
        messagebox.showinfo(
            title="Confirmacion",
            message=f"Usuario creado corrrectamente \n Usuario: {name} \n Email: {email} \n Dominio: {domain} \n Password: {passwd}"
            )
        
         
        
