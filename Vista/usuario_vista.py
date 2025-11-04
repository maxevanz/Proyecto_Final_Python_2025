import tkinter as tk
from tkinter import ttk, messagebox
from Controlador.usuarioControlador import UsuarioControlador
from Modelo.usuario import UsuarioModelo
from Utilidades.validador_campos import ValidadorCampos

class VistaUsuario(tk.Frame):
    def __init__(self, master=None, usuario_Actual=None):
        super().__init__(master)
        self.controlador = UsuarioControlador()
        self.usuario_actual = usuario_Actual
        self.usuario_id = None

        self.grid(row=0, column=0, sticky="nsew")              
        self.crear_formulario()
        self.mostrar_grilla()


    ######METODOS###########
    def crear_formulario(self):

        ####SECCION LABEL Y ENTRYS####
        self.controles_formulario = tk.Frame(self)
        self.controles_formulario.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        
        tk.Label(self.controles_formulario, text="Nombre de Usuario: ").grid(row=0, column=0, sticky="e")
        # #validacion
        vcmd = self.register(ValidadorCampos.caracteres_permitidos)
        self.nombre_usuario_entry = tk.Entry(self.controles_formulario, validate="key", validatecommand=(vcmd, "%P"), width=50)
        self.nombre_usuario_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Contraseña: ").grid(row=1, column=0, sticky="e")
        self.contraseña_entry = tk.Entry(self.controles_formulario, width=50, show="*")
        self.contraseña_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Rol: ").grid(row=2, column=0, sticky="e")
        self.rol_combo = ttk.Combobox(self.controles_formulario, width=30, values=["admin", "supervisor", "usuario", "propietario"], state="readonly")
        self.rol_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.rol_combo.current(0)

        tk.Label(self.controles_formulario, text="Estado: ").grid(row=3, column=0, sticky="e")
        self.estado_var = tk.BooleanVar(value=True)
        self.estado_check = tk.Checkbutton(self.controles_formulario, variable=self.estado_var, state=tk.DISABLED)
        self.estado_check.grid(row=3, column=1, padx=5)

        tk.Label(self.controles_formulario, text="Empleado: ").grid(row=4, column=0, sticky="e")
        self.empleado_combo = ttk.Combobox(self.controles_formulario, width=30, state="readonly")
        self.empleado_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.cargar_empleados_disponibles()

        ####SECCION BOTONES####

        self.botones_frame = tk.Frame(self)
        self.botones_frame.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.boton_crear = tk.Button(self.botones_frame, text="Crear Usuario", command=self.crear_usuario)
        self.boton_crear.grid(row=0, column=0, pady=5)

        self.boton_editar = tk.Button(self.botones_frame, text="Editar Usuario", command=self.editar_usuario)
        self.boton_editar.grid(row=1, column=0, pady=5)

        self.boton_eliminar = tk.Button(self.botones_frame, text="Activar/Desactivar Usuario", command=self.eliminar_usuario)
        self.boton_eliminar.grid(row=2, column=0, pady=5)

        self.boton_eliminar = tk.Button(self.botones_frame, text="Limpiar", command=self.limpiar_formulario)
        self.boton_eliminar.grid(row=3, column=0, pady=5)

        ###Seccion Busqueda###
        self.busqueda_frame = tk.Frame(self)
        self.busqueda_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.busqueda_frame.columnconfigure(1, weight=1)

        tk.Label(self.busqueda_frame, text="Buscar: ").grid(row=0, column=0, sticky="w", padx=5)
        self.buscar_var = tk.StringVar()
        self.buscar_entry = tk.Entry(self.busqueda_frame, textvariable=self.buscar_var)
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.buscar_var.trace_add("write", self.buscar_usuario)

    def mostrar_grilla(self):       
        columnas = ("Id", "Usuario", "Rol", "Estado", "Empleado")
        self.grilla = ttk.Treeview(self, columns=columnas, show="headings")
        self.grilla.grid(row=1, column=0, columnspan=2, padx=11, pady=10, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for col in columnas:
            self.grilla.heading(col, text=col.capitalize())
            self.grilla.column(col, width=100, anchor="center")

        self.grilla.bind("<<TreeviewSelect>>", self.seleccionar_usuario)
        self.grilla.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.cargar_usuarios()

    def seleccionar_usuario(self, event):
        seleccionado = self.grilla.focus()
        self.boton_crear.config(state=tk.DISABLED)

        if not seleccionado:
            return 
        valores = self.grilla.item(seleccionado, "values")
        self.usuario_id = valores[0]
        self.nombre_usuario_entry.config(state="normal")
        self.nombre_usuario_entry.delete(0, tk.END)
        self.nombre_usuario_entry.insert(0, valores[1])
        self.nombre_usuario_entry.config(state=tk.DISABLED)
        self.contraseña_entry.delete(0, tk.END)
        self.contraseña_entry.insert(0, self.contraseñas_por_id.get(int(valores[0]), ""))
        self.rol_combo.set(valores[2])
        self.estado_var.set(str(valores[3]) == "Activo")
        self.empleado_combo.set(valores[4])
        self.empleado_combo.config(state=tk.DISABLED)


    def cargar_usuarios(self):
        self.contraseñas_por_id = {}  # ← nuevo diccionario
        self.grilla.tag_configure("Inactivo", background="#f2dede")  # rojo claro

        for row in self.grilla.get_children():
            self.grilla.delete(row)
        self.usuarios = self.controlador.obtener_usuarios()
        
        for usuario in self.usuarios:
            if usuario[0] != self.usuario_actual:
                # Guardar contraseña por ID
                self.contraseñas_por_id[usuario[0]] = usuario[2]  # usuario[0] = id, usuario[2] = contraseña

                # Insertar solo columnas visibles
                estado = usuario[4]  # ahora el estado está en la posición 4
                tag = "Inactivo" if estado == 0 else ""
                estado_texto = "Activo" if estado == 1 else "Inactivo"
                valores = (usuario[0], usuario[1], usuario[3], estado_texto, usuario[5])  # omitimos la contraseña
                self.grilla.insert("", tk.END, values=valores, tags=(tag,))

    def buscar_usuario(self, *args):
        texto = self.buscar_var.get().lower()

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        for usuario in self.usuarios:
            # Guardar contraseña por ID
            self.contraseñas_por_id[usuario[0]] = usuario[2]  # usuario[0] = id, usuario[2] = contraseña

            # Insertar solo columnas visibles
            estado = usuario[4]  # ahora el estado está en la posición 4
            tag = "Inactivo" if estado == 0 else ""
            estado_texto = "Activo" if estado == 1 else "Inactivo"
            valores = f"{usuario[0]} {usuario[1]} {usuario[3]} {estado_texto} {usuario[5]}" # omitimos la contraseña
            if texto in valores:
                 self.grilla.insert(
                     "",tk.END,
                     values=(usuario[0], usuario[1], usuario[3], estado_texto, usuario[5]),
                     tags=(tag,)
                 )

    def cargar_empleados_disponibles(self):
        empleados = self.controlador.obtener_empleados_disponibles()
        self.empleado_map = {}      #Mapea "Apellido, Nombre" -> id
        opciones = []

        for emp_id, apellido, nombre in empleados:
            etiqueta = f"{apellido}, {nombre}"
            opciones.append(etiqueta)
            self.empleado_map[etiqueta] = emp_id

        self.empleado_combo["values"] = opciones
        if opciones:
            self.empleado_combo.current(0)

    def crear_usuario(self):
        nombreusuario = self.nombre_usuario_entry.get().strip()
        contraseña = self.contraseña_entry.get().strip()
        rol = self.rol_combo.get()
        estado = self.estado_var.get()
        empleado_etiqueta = self.empleado_combo.get()

        #validacion
        if not nombreusuario or not contraseña or not empleado_etiqueta:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        id_empleado = self.empleado_map.get(empleado_etiqueta)
        usuario = UsuarioModelo(
            nombreusuario = nombreusuario,
            contraseña = contraseña,
            rol = rol,
            estado = estado,
            id_empleado = id_empleado
        )

        exito, mensaje = self.controlador.crear_usuario(usuario)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_empleados_disponibles()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", mensaje)

    def editar_usuario(self):
        if not self.usuario_id:
            messagebox.showerror("Error","Seleecione un usuario para editar")
            return
        
        #Validacion igual que en crear usuario
        usuario = UsuarioModelo(
            id = self.usuario_id,
            contraseña = self.contraseña_entry.get().strip(),
            rol = self.rol_combo.get(),
        )
        
        exito, mensaje = self.controlador.editar_usuario(usuario)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
            self.cargar_empleados_disponibles()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_usuario(self):
        if not self.usuario_id:
            messagebox.showerror("Error", "Debe seleccionar un usuario.")
            return
        
        if not hasattr(self, "usuario_id"):
            messagebox.showerror("Error", "Seleccionar un usuario para eliminar")
            return
        
        exito, mensaje = self.controlador.activar_desactivar_usuario(self.usuario_id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_usuarios()
            self.cargar_empleados_disponibles()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.boton_crear.config(state=tk.NORMAL)
        self.nombre_usuario_entry.config(state=tk.NORMAL)
        self.empleado_combo.config(state=tk.NORMAL)

        self.usuario_id = None
        self.nombre_usuario_entry.delete(0, tk.END)
        self.contraseña_entry.delete(0, tk.END)
        self.rol_combo.current(0)
        self.estado_var.set(True)
        self.empleado_combo.set("")
        self.buscar_entry.delete(0, tk.END)
        self.buscar_var.set("")

        self.nombre_usuario_entry.focus()
        