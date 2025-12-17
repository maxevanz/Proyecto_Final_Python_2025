# import tkinter as tk
# from tkinter import messagebox
# from Modelo.usuario import UsuarioModelo
# from Controlador.usuarioControlador import UsuarioControlador

# class LoginFrame(tk.Frame):
#     def __init__(self, master, mostrar_pantalla_principal):
#         super().__init__(master)
#         print("LoginFrame cargado")  # ← esto debería aparecer en consola
#         self.controlador = UsuarioControlador()
#         self.mostrar_pantalla_principal = mostrar_pantalla_principal

#         tk.Label(self, text="Usuario:").grid(row=0, column=0)
#         self.usuario_entry = tk.Entry(self)
#         self.usuario_entry.grid(row=0, column=1)

#         tk.Label(self, text="Contraseña:").grid(row=1, column=0)
#         self.contrasena_entry = tk.Entry(self, show="*")
#         self.contrasena_entry.grid(row=1, column=1)

#         tk.Button(self, text="Ingresar", command= self.verificar_login). grid(row=2, column=0, columnspan=2)

#     def verificar_login(self):
#         usuario = self.usuario_entry.get()
#         contrasena = self.contrasena_entry.get()

#         usuario_actual = UsuarioControlador.verificar_usuario(usuario, contrasena)

#         if usuario_actual:

#             self.pack_forget()
#             self.mostrar_pantalla_principal(usuario_actual["id"], usuario_actual["NombreUsuario"], usuario_actual["Rol"])    # ← pasamos el nombre
#         else:
#             messagebox.showerror("ERROR","Credenciales Incorrectas")


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
from Modelo.usuario import UsuarioModelo
from Controlador.usuarioControlador import UsuarioControlador
from Utilidades.icon_loader import cargar_icono


version = "1.0.0"   # Versión de la aplicación


class LoginFrame(tk.Frame):
    def __init__(self, master, mostrar_pantalla_principal):
        super().__init__(master, bg="#333333")
        print("LoginFrame cargado")
        self.icon_ingresar = cargar_icono("boton-ingresar.png")
        self.icon_registrar = cargar_icono("boton-registrar.png")

        self.controlador = UsuarioControlador()
        self.mostrar_pantalla_principal = mostrar_pantalla_principal

        self.contraseña_visible = False


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        contenedor = tk.Frame(self, bg="#333333")
        contenedor.grid(row=0, column=0, sticky="nsew")
        contenedor.grid_columnconfigure(0, weight=1)


        estilo_label = {
            "font": ("Segoe UI", 15),
            "bg": "#333333",
            "fg": "#FFFFFF"
        }

        estilo_entry = {
            "font": ("Segoe UI", 15),
            "bg": "#444444",
            "fg": "white",
            "insertbackground": "white",
            "relief": "flat",
            "width": 20
        }


        titulo = tk.Label(contenedor, text="Iniciar Sesión",
                          font=("Segoe UI", 22, "bold"),
                          bg="#333333", fg="white")
        titulo.grid(row=0, column=0, pady=(30, 40))

        lbl_usuario = tk.Label(contenedor, text="Usuario:", **estilo_label)
        lbl_usuario.grid(row=1, column=0, sticky="w", padx=80)

        self.usuario_entry = tk.Entry(contenedor, **estilo_entry)
        self.usuario_entry.grid(row=2, column=0, pady=(0, 25), padx=80, sticky="ew")

        lbl_contra = tk.Label(contenedor, text="Contraseña:", **estilo_label)
        lbl_contra.grid(row=3, column=0, sticky="w", padx=80)

        password_frame = tk.Frame(contenedor, bg="#333333")
        password_frame.grid(row=4, column=0, padx=80, pady=(0, 35), sticky="ew")
        password_frame.grid_columnconfigure(0, weight=1)

        self.contrasena_entry = tk.Entry(password_frame, show="*", **estilo_entry)
        self.contrasena_entry.grid(row=0, column=0, sticky="ew")


        self.btn_mostrar = tk.Button(
            password_frame,
            text="     👁️",
            bg="#444444",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat",
            width=3,
            command=self.toggle_password
        )
        self.btn_mostrar.grid(row=0, column=1, padx=(10, 0))

        btn_ingresar = tk.Button(
            contenedor,
            text="Ingresar",
            bg="#9233FF",   
            fg="#FFFFFF",
            font=("Segoe UI", 15, "bold"),
            relief="flat",
            padx=10,
            pady=8,
            image=self.icon_ingresar, compound="right",
            command=self.verificar_login
        )
        btn_ingresar.grid(row=5, column=0, pady=(0, 10))

        btn_registrar = tk.Button(
            contenedor,
            text="Registrar",
            bg="#555555",
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            image=self.icon_registrar, compound="right",
            command=self.abrir_registro_web
        )
        btn_registrar.grid(row=6, column=0, pady=(0, 30))

        lbl_version = tk.Label(
            self,
            text=f"Versión {version}",
            font=("Segoe UI", 10),
            bg="#333333",
            fg="#888888"
        )
        lbl_version.grid(row=1, column=0, sticky="se", padx=10, pady=5)


    def toggle_password(self):
        if self.contraseña_visible:
            self.contrasena_entry.config(show="*")
            self.btn_mostrar.config(text="     👁️")
        else:
            self.contrasena_entry.config(show="")
            self.btn_mostrar.config(text="✔️")

        self.contraseña_visible = not self.contraseña_visible


    def abrir_registro_web(self):
        webbrowser.open("https://www.google.com")

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        usuario_actual = UsuarioControlador.verificar_usuario(usuario, contrasena)

        if usuario_actual:
            self.pack_forget()
            self.mostrar_pantalla_principal(
                usuario_actual["id"],
                usuario_actual["NombreUsuario"],
                usuario_actual["Rol"]
            )
        else:
            messagebox.showerror("ERROR", "Credenciales Incorrectas")
