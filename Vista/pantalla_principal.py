import tkinter as tk
from Vista.empleado_vista import VistaEmpleado

class PantallaPrincipalFrame(tk.Frame):
    def __init__(self, master, mostrar_login):
        super().__init__(master)
        self.master = master     
        self.mostrar_login = mostrar_login

        self.menu_creado = False
       
        #Area de contenido
        self.contenido = tk.Frame(self)
        self.contenido.pack(fill=tk.BOTH, expand=True)

    def pantalla_bienvenida(self):
        self.limpiar_contenido()
        tk.Label(self.contenido, text="Bienvenido al Sistema de Portería").pack(pady=20)

    def crear_menu(self):
        #Menu Principal
        self.menu = tk.Menu(self.master)
        self.master.config(menu = self.menu)

        #Menu de "gestion"
        menu_gestion = tk.Menu(self.menu, tearoff=0)
        menu_gestion.add_cascade(label="Empleados", command=self.mostrar_empleados)
        menu_gestion.add_cascade(label="Eventos", command=self.mostrar_eventos)
        self.menu.add_cascade(label="Gestión", menu=menu_gestion)

        #Menu de "Cuenta"
        menu_cuenta = tk.Menu(self.menu, tearoff=0)
        menu_cuenta.add_cascade(label="Cerrar Sesión", command=self.cerrar_sesion)
        self.menu.add_cascade(label="Cuenta", menu=menu_cuenta)

    def mostrar_menu(self):
        self.pack(fill=tk.BOTH, expand=True)
        if not self.menu_creado:
            self.crear_menu()
            self.menu_creado = True
        self.pantalla_bienvenida()

    def mostrar_empleados(self):
        self.limpiar_contenido()
        vista = VistaEmpleado(self.contenido)
        vista.pack(fill=tk.BOTH, expand=True)

    def mostrar_eventos(self):
        pass

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
        self.pack_forget()
        self.mostrar_login()