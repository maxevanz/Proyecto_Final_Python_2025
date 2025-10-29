import tkinter as tk
<<<<<<< HEAD
from tkinter import Menu
from Vista.empleado_vista import VistaEmpleado
from Vista.usuario_vista import VistaUsuario
=======
from Vista.empleado_vista import VistaEmpleado
>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472

class PantallaPrincipalFrame(tk.Frame):
    def __init__(self, master, mostrar_login):
        super().__init__(master)
        self.master = master     
        self.mostrar_login = mostrar_login
<<<<<<< HEAD
=======

>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472
        self.menu_creado = False
       
        #Area de contenido
        self.contenido = tk.Frame(self)
        self.contenido.pack(fill=tk.BOTH, expand=True)

<<<<<<< HEAD
    def set_usuario(self, nombre_usuario, rol):
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
        self.menu.add_cascade(label="Gestión", menu=menu_gestion)

        #Menu de "Cuenta"
        menu_cuenta = Menu(self.menu, tearoff=0)
        menu_cuenta.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        self.menu.add_cascade(label="Cuenta", menu=menu_cuenta)
        
        #Mostrar usuario actual
        self.menu.add_command(label=f"Usuario: {self.usuario_actual}", state="disabled")
=======
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
>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472

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

<<<<<<< HEAD
    def mostrar_usuarios(self):
        self.limpiar_contenido()
        vista = VistaUsuario(self.contenido)
        vista.pack(fill=tk.BOTH, expand=True)
    
=======
>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472
    def mostrar_eventos(self):
        pass

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
<<<<<<< HEAD
        # Reemplaza el menú por uno vacío
        self.master.config(menu=tk.Menu(self.master))
        self.master.config(menu=None)
        self.menu_creado = False
        self.menu = None
        self.pack_forget()
        self.mostrar_login()
        print("Menú actual tras limpieza:", self.master["menu"])


=======
        self.pack_forget()
        self.mostrar_login()
>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472
