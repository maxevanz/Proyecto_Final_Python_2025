import tkinter as tk
from tkinter import messagebox
from Modelo.usuario import UsuarioModelo
from Controlador.usuarioControlador import UsuarioControlador

class LoginFrame(tk.Frame):
    def __init__(self, master, mostrar_pantalla_principal):
        super().__init__(master)
        print("LoginFrame cargado")  # ← esto debería aparecer en consola
        self.controlador = UsuarioControlador()
        self.mostrar_pantalla_principal = mostrar_pantalla_principal

        tk.Label(self, text="Usuario:").grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(self, text="Contraseña:").grid(row=1, column=0)
        self.contrasena_entry = tk.Entry(self, show="*")
        self.contrasena_entry.grid(row=1, column=1)

        tk.Button(self, text="Ingresar", command= self.verificar_login). grid(row=2, column=0, columnspan=2)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        usuario_actual = UsuarioControlador.verificar_usuario(usuario, contrasena)

        if usuario_actual:

            self.pack_forget()
            self.mostrar_pantalla_principal(usuario_actual["id"], usuario_actual["NombreUsuario"], usuario_actual["Rol"])    # ← pasamos el nombre
        else:
            messagebox.showerror("ERROR","Credenciales Incorrectas")