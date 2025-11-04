import tkinter as tk
from tkinter import Menu
from Vista.empleado_vista import VistaEmpleado
from Vista.usuario_vista import VistaUsuario
#from Vista.evento_vista import VistaEvento
from  Vista.evento_tarjeta_vista import VistaEventoTarjeta
from Vista.evento_admin_vista import VistaAdminEvento

class PantallaPrincipalFrame(tk.Frame):
    def __init__(self, master, mostrar_login):
        super().__init__(master)
        self.master = master     
        self.mostrar_login = mostrar_login
        self.menu_creado = False
       
        #Area de contenido
        self.contenido = tk.Frame(self)
        self.contenido.pack(fill=tk.BOTH, expand=True)

    def set_usuario(self, id_usuario, nombre_usuario, rol):
        self.id_usuario_actual = id_usuario
        self.usuario_actual = nombre_usuario
        self.rol_actual = rol

    def pantalla_bienvenida(self):
        self.limpiar_contenido()
        mensaje = f"Bienvenido al Sistema de Portería \n Sesión iniciada como: {self.usuario_actual}"
        tk.Label(self.contenido, text=mensaje, font=("Arial", 12)).pack(pady=20)

    def crear_menu(self):
        #Menu Principal
        self.menu = Menu(self.master)
        self.master.config(menu = self.menu)

        #Menu de "gestion"
        menu_gestion = Menu(self.menu, tearoff=0)
        if self.rol_actual == "admin":
            menu_gestion.add_command(label="Empleados", command=self.mostrar_empleados)            
            menu_gestion.add_command(label="Usuarios", command=self.mostrar_usuarios)
            menu_gestion.add_command(label="Eventos", command=self.mostrar_eventos)
        elif self.rol_actual == "usuario":
            menu_gestion.add_command(label="Eventos", command=self.mostrar_eventos)
        elif self.rol_actual == "propietario":
            menu_gestion.add_command(label="Expensas", command="")
            menu_gestion.add_command(label="Reclamos", command="")
            menu_gestion.add_command(label="Novedades", command="")
            
        self.menu.add_cascade(label="Gestión", menu=menu_gestion)

        

        #Menu de "Cuenta"
        menu_cuenta = Menu(self.menu, tearoff=0)
        menu_cuenta.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        self.menu.add_cascade(label="Cuenta", menu=menu_cuenta)
        
        #Mostrar usuario actual
        self.menu.add_command(label=f"Usuario: {self.usuario_actual} - Rol: {self.rol_actual} - Id: {self.id_usuario_actual}", state="disabled")

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

    def mostrar_usuarios(self):
        self.limpiar_contenido()
        vista = VistaUsuario(self.contenido, self.id_usuario_actual)
        vista.pack(fill=tk.BOTH, expand=True)
    
    def mostrar_eventos(self):
        # self.limpiar_contenido()
        # vista = VistaEvento(self.contenido, id_usuario = self.id_usuario_actual)
        # vista.pack(fill=tk.BOTH, expand=True)

        # self.limpiar_contenido()
        # vista = VistaEventoTarjeta(self.contenido, self.id_usuario_actual)
        # vista.pack(fill=tk.BOTH, expand=True)

        self.limpiar_contenido()
        vista = VistaAdminEvento(self.contenido, self.id_usuario_actual)
        vista.pack(fill=tk.BOTH, expand=True)

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
        # Reemplaza el menú por uno vacío
        self.master.config(menu=tk.Menu(self.master))
        self.master.config(menu=None)
        self.menu_creado = False
        self.menu = None
        self.pack_forget()
        self.mostrar_login()
        print("Menú actual tras limpieza:", self.master["menu"])


