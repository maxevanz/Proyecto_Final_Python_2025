import tkinter as tk
from tkinter import ttk, messagebox
from Controlador.empleadoControlador import EmpleadoControlador
from Modelo.empleado import EmpleadoModelo
from Utilidades.validador_campos import ValidadorCampos


class VistaEmpleado(tk.Frame):
    #####INICIALIZADOR
    def __init__(self, master):
        super().__init__(master)
        self.controlador = EmpleadoControlador()
        self.empleado_seleccionado = None

        ###Cargar Formulario###
        self.crear_formulario()

        #Mostrar la lista de empleados
        self.mostrar_grilla()
        self.grilla.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        #Pintar las filas inactivas
        #self.grilla.tag_configure("estado0", foreground="red")  # para pintar los empleados Inactivos
        self.grilla.tag_configure("estado0", background="#f2dede")  # rojo claro


    ######METODOS###########
    def crear_formulario(self):

        
        ######Seccion Formulario(label y entrys)
        self.controles_formulario = tk.Frame(self)
        self.controles_formulario.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        tk.Label(self.controles_formulario, text="Empleados", font=("Arial", 12)).grid(row=0, column=0, sticky="e")

        tk.Label(self.controles_formulario, text="Apellido:").grid(row=1, column=0, sticky="e")
        self.apellido_entry = tk.Entry(self.controles_formulario, width=50)
        self.apellido_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Nombre:").grid(row=2, column=0, sticky="e")
        self.nombre_entry = tk.Entry(self.controles_formulario, width=50)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Correo:").grid(row=3, column=0, sticky="e")
        self.correo_entry = tk.Entry(self.controles_formulario, width=50)
        self.correo_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Telefono:").grid(row=4, column=0, sticky="e")
        #validacion
        vcmd = self.register(ValidadorCampos.validar_telefono)
        self.telefono_entry = tk.Entry(self.controles_formulario, validate="key", validatecommand=(vcmd, "%P"), width=50)
        self.telefono_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Estado:").grid(row=5, column=0, sticky="e")
        self.estado_var = tk.BooleanVar()
        self.estado_check = tk.Checkbutton(self.controles_formulario, text="Estado", variable=self.estado_var, state=tk.DISABLED)
        self.estado_check.grid(row=5, column=1, sticky="w")


        ####Seccion Botones
        self.botones = tk.Frame(self)
        self.botones.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.boton_crear = tk.Button(self.botones, text="Crear", command=self.nuevo_empleado)
        self.boton_crear.grid(row=0, column=0, pady=5)
        self.boton_editar = tk.Button(self.botones, text="Editar", command=self.editar_empleado)
        self.boton_editar.grid(row=1, column=0, pady=5)
        self.boton_eliminar = tk.Button(self.botones, text="Eliminar", command=self.eliminar_empleado)
        self.boton_eliminar.grid(row=2, column=0, pady=5)
        self.boton_limpiar = tk.Button(self.botones, text="Limpiar", command=self.limpiar_campos)
        self.boton_limpiar.grid(row=3, column=0, pady=5)

        ###Seccion Busqueda###
        self.busqueda_frame = tk.Frame(self)
        self.busqueda_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.busqueda_frame.columnconfigure(1, weight=1)

        tk.Label(self.busqueda_frame, text="Buscar: ").grid(row=0, column=0, sticky="w", padx=5)
        self.buscar_var = tk.StringVar()
        self.buscar_entry = tk.Entry(self.busqueda_frame, textvariable=self.buscar_var)
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.buscar_var.trace_add("write", self.buscar_empleados)

    def mostrar_grilla(self):
        # TreeView para mostrar empleados
        self.grilla = ttk.Treeview(self, columns=("id","Apellido","Nombre","Correo","Telefono","Estado"), show="headings")
        self.grilla.grid(row=6, column=0, columnspan=2, padx=1, pady=10, sticky="nsew")
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for col in ("id","Apellido","Nombre","Correo","Telefono","Estado"):
            self.grilla.heading(col, text=col)
            self.grilla.column(col, width=100)

        self.grilla.bind("<<TreeviewSelect>>", self.seleccionar_empleado)

        self.actualizar_lista()

    def actualizar_lista(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)
        self.empleados = self.controlador.obtener_todos()

        for empleado in self.empleados:
            estado_legible = "Activo" if str(empleado.estado) == "1" else "Inactivo"
            tag = "estado0" if str(empleado.estado) == "0" else ""
            self.grilla.insert(
                "", 
                tk.END, 
                values=(empleado.id, empleado.apellido, empleado.nombre, empleado.correo, empleado.telefono, estado_legible),
                tags=(tag,))

    def seleccionar_empleado(self, event):
        seleccion = self.grilla.selection()
        self.estado_check.config(state=tk.NORMAL)
        self.boton_crear.config(state = tk.DISABLED)

        if seleccion:
            item = seleccion[0]
            valores = self.grilla.item(item)["values"]   
            estado = valores[5] #columna Estado        
            print("seleccionado: ", valores) 

            #Buscar el empleado en la lista
            empleado_id = valores[0]
            self.empleado_seleccionado = next((e for e in self.empleados if e.id == empleado_id), None)

            if self.empleado_seleccionado:
                
                self.apellido_entry.delete(0, tk.END)
                self.apellido_entry.insert(0, self.empleado_seleccionado.apellido)

                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, self.empleado_seleccionado.nombre)

                self.correo_entry.delete(0, tk.END)
                self.correo_entry.insert(0, self.empleado_seleccionado.correo)

                self.telefono_entry.delete(0, tk.END)
                self.telefono_entry.insert(0, self.empleado_seleccionado.telefono)
                self.estado_var.set(str(valores[5]) == "Activo")  # actualiza el valor según estado

    def buscar_empleados(self, *args):
        texto = self.buscar_var.get().lower()

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        for e in self.empleados:
            estado_legible = "Activo" if str(e.estado) == "1" else "Inactivo"
            tag = "estado0" if str(e.estado) == "0" else ""

            #Convertir todos los campos a texto y buscar coincidencias
            valores = f"{e.apellido} {e.nombre} {e.correo} {e.telefono} {estado_legible}".lower()
            if texto in valores:
                self.grilla.insert(
                    "",tk.END,
                    values=(e.id, e.apellido, e.nombre, e.correo, e.telefono, estado_legible),
                    tags=(tag,)
                )
    
    def nuevo_empleado(self):

        apellido = self.apellido_entry.get()
        nombre = self.nombre_entry.get()
        correo = self.correo_entry.get()
        telefono = self.telefono_entry.get()
        estado = 1

        #validacion
        if not apellido or not nombre or not correo:
            messagebox.showerror("Atención","Todos los campos son obligatorios.")
            return
        empleado = EmpleadoModelo(
            apellido=apellido,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            estado=estado
        )

        exito, mensaje = self.controlador.nuevo_empleado(empleado)
        messagebox.showinfo("Resultado", mensaje)
        
        if exito:
            self.actualizar_lista()
            self.limpiar_campos()

    def editar_empleado(self):
        if not self.empleado_seleccionado:
            messagebox.showerror("Advertencia","Debe seleccionar un empleado")
            return
        
        #Validacion
        empleado = EmpleadoModelo(
            id=self.empleado_seleccionado.id,
            apellido=self.apellido_entry.get(),
            nombre=self.nombre_entry.get(),
            correo=self.correo_entry.get(),
            telefono=self.telefono_entry.get(),
            estado= 1 if self.estado_var.get() else 0
        )

        exito, mensaje = self.controlador.editar_empleado(empleado)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_lista()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_empleado(self):
        if not self.empleado_seleccionado:
            messagebox.showerror("Error","Debe seleccionar un empleado")
            return
        
        if not hasattr(self, 'empleado_seleccionado'):
            messagebox.showerror("Error","Debe seleccionar un empleado")
            return
        
        exito, mensaje = self.controlador.eliminar_empleado(self.empleado_seleccionado.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_lista()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)
            
    def limpiar_campos(self):

        self.empleado_seleccionado = None
        self.apellido_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.buscar_entry.delete(0, tk.END)
        self.buscar_var.set("")
        self.apellido_entry.focus()

        self.estado_check.config(state=tk.DISABLED)
        self.estado_var.set(False)
        self.boton_crear.config(state=tk.ACTIVE)
