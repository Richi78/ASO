
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Controlador.generalConfigs import installApache,installFTP,installPostGreSQL
from Utils.utils import generatePassword, createDirectoryWeb, verifyUser, createVirtualHost, restartApache, modifyHosts
from DB.postgres import  configure_postgresql, configure_pg_hba,  connect_to_db
from Controlador.userController import addUserToJson, listUsers, getUserByName,deleteUser

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
        self.userDB = tk.StringVar(value="")
        self.passwd = tk.StringVar(value="")
        self.userQuota = tk.StringVar(value="")
        self.userToDelete = tk.StringVar(value="")
        self.userToUpdate = tk.StringVar(value="")

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

        # Frame userDB

        self.frame_userDB = tk.Frame(
            self.master,
            width=700,
            height=200,
            pady=5
        )
        self.frame_userDB.pack()

        self.label_userDB = tk.Label(
            self.frame_userDB,
            text="Base de datos"
            )
        self.label_userDB.pack(side="left")

        self.combo_DB = ttk.Combobox(
            self.frame_userDB,
            values=['PostgreSQL','MySQL'],
            state="readonly",
            textvariable=self.userDB
        )
        self.combo_DB.pack()
    
        # Frame Quota
        
        self.frame_userQuota = tk.Frame(
            self.master,
            width=700,
            height=200,
            pady=5
        )
        self.frame_userQuota.pack()

        self.label_userQuota = tk.Label(
            self.frame_userQuota,
            text="Espacio de disco"
            )
        self.label_userQuota.pack(side="left")

        self.combo_Quota = ttk.Combobox(
            self.frame_userQuota,
            values=['200MB','500MB', '1GB'],
            state="readonly",
            textvariable=self.userQuota
        )
        self.combo_Quota.pack()

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

        # Frame addons
        self.frame_addons = tk.Frame(
            self.master, 
            width=700, 
            height=200,
            pady=5
            )
        self.frame_addons.pack()

        self.button_listUsers = tk.Button(
            self.frame_addons,
            text="Listar usuarios",
            command=self.handleListUsers
        )
        self.button_listUsers.pack(side="left")

        self.button_updateUser = tk.Button(
            self.frame_addons,
            text="Editar usuario",
            command=self.handleUpdateUser
        )
        self.button_updateUser.pack(side="left")

        self.button_deleteUser = tk.Button(
            self.frame_addons,
            text="Eliminar usuario",
            command=self.handleDeleteUser
        )
        self.button_deleteUser.pack(side="left")

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
        quote = self.userQuota.get()
        db = self.userDB.get()
        status = verifyUser(name=name, email=email, domain=domain, passwd=passwd, db=db, quote=quote)
        if status["status"] == 400:
            messagebox.showerror(
                title="Error",
                message=status["message"]
            )
            return
        addUserToJson(name=name, email=email, domain=domain, passwd=passwd, db=db, diskQuote=quote)
        createDirectoryWeb(name)
        createVirtualHost(name=name, email=email, domain=domain)
        modifyHosts(domain=domain)
        restartApache()
        configure_postgresql(db_name=name, db_user=name, db_password=passwd)
        configure_pg_hba(db_name=name, db_user=name)
        messagebox.showinfo(
            title="Confirmacion",
            message=f"Usuario creado corrrectamente \n Usuario: {name} \n Email: {email} \n Dominio: {domain} \n Password: {passwd}"
            )
        self.clearAllVariables()
        
    def handleListUsers(self):
        allUsers = listUsers()
        listUsers_window = tk.Toplevel()
        listUsers_window.geometry("400x450")
        listUsers_window.title("Usuarios")
        
        label_list = tk.Label(
            listUsers_window,
            text="Lista de usuarios"
            )
        label_list.pack()
        
        for e in allUsers:
            label_user = tk.Label(
                listUsers_window,
                text=e,
                pady=5
            )
            label_user.pack()

        button = tk.Button(
            listUsers_window,
            text="Aceptar",
            command= lambda: listUsers_window.destroy(),
            pady=5,
            )
        button.pack()
    
    def handleDeleteUser(self):
        delete_window = tk.Toplevel()
        delete_window.geometry("200x100")
        delete_window.title("Eliminar usuario")

        label = tk.Label(
            delete_window,
            text="Ingrese usuario"
            )
        label.pack()

        entry = tk.Entry(
            delete_window,
            textvariable=self.userToDelete
            )
        entry.pack()

        button = tk.Button(
            delete_window,
            text="Eliminar",
            command=lambda: confirm()
            )
        button.pack()

        def confirm():
            inputText = self.userToDelete.get()
            user = getUserByName(name=inputText)
            if not user:          
                messagebox.showerror(
                    title="Error",
                    message=f"El usuario no existe"
                )
                return

            result = messagebox.askyesno(
                title="Confirmacion",
                message=f"Estas seguro de eliminar el usuario {self.userToDelete.get()}?"
                )
            
            if result:
                status = deleteUser(user=user)
                messagebox.showinfo(
                    title="Confirmacion",
                    message=status["message"]
                )
                delete_window.destroy()

    def handleUpdateUser(self):
        update_window = tk.Toplevel()
        update_window.geometry("300x400")
        update_window.title("Editar usuario")

        label = tk.Label(
            update_window,
            text="Ingrese usuario"
            )
        label.pack()

        entry = tk.Entry(
            update_window,
            textvariable=self.userToUpdate
            )
        entry.pack()

        button = tk.Button(
            update_window,
            text="Editar",
            command=lambda: getInfo()
            )
        button.pack()

        def getInfo():
            inputText = self.userToUpdate.get()
            user = getUserByName(inputText)
            if not user:
                messagebox.showerror(
                    title="Error",
                    message=f"El usuario no existe"
                )
                return
            newName = tk.StringVar(value=user["name"])
            newEmail = tk.StringVar(value=user["email"])
            newDomain = tk.StringVar(value=user["domain"])
            newPasswd = tk.StringVar(value=user["password"])
            newDB = tk.StringVar(value=user["database"])
            newQuote = tk.StringVar(value=user["diskQuote"])
            entry.config(state="disabled")
            button.config(state="disabled")
            # editar nombre
            label_Name = tk.Label(update_window, text="Nombre de usuario")
            label_Name.pack()
            entry_Name = tk.Entry(update_window, textvariable=newName)
            entry_Name.pack()
            
            # editar correo
            label_Email = tk.Label(update_window, text="Correo electronico")
            label_Email.pack()
            entry_Email = tk.Entry(update_window, textvariable=newEmail)
            entry_Email.pack()
            
            # editar dominio
            label_Domain = tk.Label(update_window, text="Dominio")
            label_Domain.pack()
            entry_Domain = tk.Entry(update_window, textvariable=newDomain)
            entry_Domain.pack()
    
            # editar password
            label_Passwd = tk.Label(update_window, text="Password")
            label_Passwd.pack()
            entry_Passwd = tk.Entry(update_window, textvariable=newPasswd)
            entry_Passwd.pack()

            # editar db
            label_Db = tk.Label(update_window, text="Base de datos")
            label_Db.pack()
            cb_Db = ttk.Combobox(update_window, values=["PostgreSQL","MariaDB"], state="readonly")
            cb_Db.set(newDB.get())
            cb_Db.pack()
            cb_Db.bind("<<ComboboxSelected>>", lambda e: selectDB(e))

            # editar cuota
            label_quote = tk.Label(update_window, text="Espacio de disco")
            label_quote.pack()
            cb_quote = ttk.Combobox(update_window, values=["200MB","500MB","1GB"], state="readonly")
            cb_quote.set(newQuote.get())
            cb_quote.pack()
            cb_quote.bind("<<ComboboxSelected>>", lambda e: selectQuote(e))

            # button accept
            btn_accept = tk.Button(update_window, text="Guardar", command=lambda: accept())
            btn_accept.pack()
            # button cancel
            btn_cancel = tk.Button(update_window, text="Cancelar", command=lambda: cancel())
            btn_cancel.pack()

            def selectDB(event):
                newDB.set(cb_Db.get())
            def selectQuote(event):
                newQuote.set(cb_quote.get())
            def accept():
                result = messagebox.askyesno(
                    title="Confirmacion",
                    message="Estas seguro de modificar los datos?"
                )
                if result:
                    # modificar aqui :D
                    messagebox.showinfo(
                        title="Exito",
                        message="Se realizaron los cambios con exito."
                    )
                    update_window.destroy()

            def cancel():
                label_Name.destroy() ; entry_Name.destroy()
                label_Email.destroy() ; entry_Email.destroy()
                label_Domain.destroy() ; entry_Domain.destroy()
                label_Passwd.destroy() ; entry_Passwd.destroy()
                label_Db.destroy() ; cb_Db.destroy()
                label_quote.destroy() ; cb_quote.destroy()
                btn_accept.destroy() ; btn_cancel.destroy()
                entry.config(state="normal") ; button.config(state="normal")


    def clearAllVariables(self):
        self.userName.set("")
        self.userEmail.set("")
        self.userDomain.set("")
        self.userDB.set("")
        self.passwd.set("")
        self.userQuota.set("")
        self.userToDelete.set("")
        
    