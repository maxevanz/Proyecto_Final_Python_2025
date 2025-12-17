import tkinter as tk
from tkinter import ttk, messagebox
from Controlador.propietarioControlador import PropietarioControlador
from Modelo.propietario import PropietarioModelo
from Utilidades.estilos import configurar_estilos
from Utilidades.icon_loader import cargar_icono
from Utilidades.validador_campos import ValidadorCampos


class VistaPropietario(tk.Frame):
    #####INICIALIZADOR
    def __init__(self, master):
        super().__init__(master)
        self.controlador = PropietarioControlador()
        self.propietario_seleccionado = None
        configurar_estilos()

        ###Cargar Formulario###
        self.crear_formulario()


        #Mostrar la lista de empleados
        self.mostrar_grilla()
        #Pintar las filas inactivas
        #self.grilla.tag_configure("estado0", foreground="red")  # para pintar los empleados Inactivos
        self.grilla.tag_configure("estado0", background="#f2dede")  # rojo claro


    ######METODOS###########
    def crear_formulario(self):
        tk.Label(self, text="Administrar Propietarios", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="nw")

        ######Seccion Formulario(label y entrys)
        self.controles_formulario = tk.Frame(self)
        self.controles_formulario.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(self.controles_formulario, text="Apellido:").grid(row=0, column=0, sticky="e")
        self.apellido_entry = tk.Entry(self.controles_formulario, width=50)
        self.apellido_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.nombre_entry = tk.Entry(self.controles_formulario, width=50)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="DNI:").grid(row=2, column=0, sticky="e")
        #validacion
        vcmd = self.register(ValidadorCampos.validar_dni)
        self.dni_entry = tk.Entry(self.controles_formulario, validate="key", validatecommand=(vcmd, "%P"), width=50)
        self.dni_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Telefono:").grid(row=3, column=0, sticky="e")
        #validacion
        vcmd = self.register(ValidadorCampos.validar_telefono)
        self.telefono_entry = tk.Entry(self.controles_formulario, validate="key", validatecommand=(vcmd, "%P"), width=50)
        self.telefono_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(self.controles_formulario, text="Departamento:").grid(row=4, column=0, sticky="e")
        self.departamento_entry = tk.Entry(self.controles_formulario, width=30)
        self.departamento_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.controles_formulario, text="Estado:").grid(row=5, column=0, sticky="e")
        self.estado_var = tk.BooleanVar()
        self.estado_check = tk.Checkbutton(self.controles_formulario, text="Estado", variable=self.estado_var, state=tk.DISABLED)
        self.estado_check.grid(row=5, column=1, sticky="w")


        ####Seccion Botones
        self.icon_nuevo = cargar_icono("boton-agregar.png")
        self.icon_editar = cargar_icono("boton-editar.png")
        self.icon_eliminar = cargar_icono("boton-borrar.png")
        self.icon_limpiar = cargar_icono("boton-limpiar.png")

        self.botones = tk.Frame(self)
        self.botones.grid(row=1, column=1, pady=10, padx=10, sticky="e")

        self.boton_crear = ttk.Button(self.botones, text="Crear", image=self.icon_nuevo, 
                                     compound="right", style="Nuevo.TButton",
                                     command=self.nuevo_propietario)
        self.boton_crear.grid(row=0, column=0, pady=2, padx=2)
        self.boton_editar = ttk.Button(self.botones, text="Editar", image=self.icon_editar, 
                                       compound="right", style="Editar.TButton",
                                       command=self.editar_propietario)
        self.boton_editar.grid(row=1, column=0, pady=2, padx=2)
        self.boton_eliminar = ttk.Button(self.botones, text="Eliminar", image=self.icon_eliminar, 
                                         compound="right", style="Eliminar.TButton",
                                         command=self.eliminar_propietario)
        self.boton_eliminar.grid(row=2, column=0, pady=2, padx=2)
        self.boton_limpiar = ttk.Button(self.botones, text="Limpiar", image=self.icon_limpiar, 
                                        compound="right", style="Limpiar.TButton",
                                        command=self.limpiar_campos)
        self.boton_limpiar.grid(row=3, column=0, pady=2, padx=2)

        ###Seccion Busqueda###
        self.busqueda_frame = tk.Frame(self)
        self.busqueda_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.busqueda_frame.columnconfigure(1, weight=1)

        tk.Label(self.busqueda_frame, text="Buscar: ").grid(row=0, column=0, sticky="w", padx=5)
        self.buscar_var = tk.StringVar()
        self.buscar_entry = tk.Entry(self.busqueda_frame, textvariable=self.buscar_var)
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.buscar_var.trace_add("write", self.buscar_propietario)

    def mostrar_grilla(self):
        # TreeView para mostrar empleados
        columnas = ("Id","Apellido","Nombre","DNI","Telefono","Estado","Departamento")
        self.grilla = ttk.Treeview(self, columns=columnas, show="headings")
        self.grilla.grid(row=3, column=0, columnspan=2, padx=11, pady=10, sticky="nsew")
        #self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for col in columnas:
            self.grilla.heading(col, text=col.capitalize())
            self.grilla.column(col, width=100, anchor="center")

        self.grilla.bind("<<TreeviewSelect>>", self.seleccionar_propietario)
        self.grilla.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.actualizar_lista()

    def actualizar_lista(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)
        self.propietarios = self.controlador.obtener_todos()

        for propietario in self.propietarios:
            estado_legible = "Activo" if str(propietario.estado) == "1" else "Inactivo"
            tag = "estado0" if str(propietario.estado) == "0" else ""
            self.grilla.insert(
                "", 
                tk.END, 
                values=(propietario.id, propietario.apellido, propietario.nombre, propietario.dni, propietario.telefono, estado_legible, propietario.departamento),
                tags=(tag,))

    def seleccionar_propietario(self, event):
        seleccion = self.grilla.selection()
        self.estado_check.config(state=tk.NORMAL)
        self.boton_crear.config(state = tk.DISABLED)

        if seleccion:
            item = seleccion[0]
            valores = self.grilla.item(item)["values"]   
            estado = valores[5] #columna Estado        
            print("seleccionado: ", valores) 

            #Buscar el empleado en la lista
            propietario_id = valores[0]
            self.propietario_seleccionado = next((e for e in self.propietarios if e.id == propietario_id), None)

            if self.propietario_seleccionado:
                
                self.apellido_entry.delete(0, tk.END)
                self.apellido_entry.insert(0, self.propietario_seleccionado.apellido)

                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, self.propietario_seleccionado.nombre)

                self.dni_entry.delete(0, tk.END)
                self.dni_entry.insert(0, self.propietario_seleccionado.dni)

                self.telefono_entry.delete(0, tk.END)
                self.telefono_entry.insert(0, self.propietario_seleccionado.telefono)
                self.estado_var.set(str(valores[5]) == "Activo")  # actualiza el valor según estado

                self.departamento_entry.delete(0, tk.END)
                self.departamento_entry.insert(0, self.propietario_seleccionado.departamento)

    def buscar_propietario(self, *args):
        texto = self.buscar_var.get().lower()

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        for p in self.propietarios:
            estado_legible = "Activo" if str(p.estado) == "1" else "Inactivo"
            tag = "estado0" if str(p.estado) == "0" else ""

            #Convertir todos los campos a texto y buscar coincidencias
            valores = f"{p.apellido} {p.nombre} {p.dni} {p.telefono} {estado_legible} {p.departamento}".lower()
            if texto in valores:
                self.grilla.insert(
                    "",tk.END,
                    values=(p.id, p.apellido, p.nombre, p.dni, p.telefono, estado_legible, p.departamento),
                    tags=(tag,)
                )
    
    def nuevo_propietario(self):

        apellido = self.apellido_entry.get()
        nombre = self.nombre_entry.get()
        dni = self.dni_entry.get()
        telefono = self.telefono_entry.get()
        estado = 1
        departamento = self.departamento_entry.get()

        #validacion
        if not apellido or not nombre or not dni or not departamento:
            messagebox.showerror("Atención","Todos los campos son obligatorios.")
            return
        propietario = PropietarioModelo(
            apellido=apellido,
            nombre=nombre,
            dni=dni,
            telefono=telefono,
            estado=estado,
            departamento=departamento
        )

        exito, mensaje = self.controlador.nuevo_propietario(propietario)
        messagebox.showinfo("Resultado", mensaje)
        
        if exito:
            self.actualizar_lista()
            self.limpiar_campos()

    def editar_propietario(self):
        if not self.propietario_seleccionado:
            messagebox.showerror("Advertencia","Debe seleccionar un propietario")
            return
        
        #Validacion
        propietario = PropietarioModelo(
            id=self.propietario_seleccionado.id,
            apellido=self.apellido_entry.get(),
            nombre=self.nombre_entry.get(),
            dni=self.dni_entry.get(),
            telefono=self.telefono_entry.get(),
            estado= 1 if self.estado_var.get() else 0,
            departamento=self.departamento_entry.get()
        )

        exito, mensaje = self.controlador.editar_propietario(propietario)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_lista()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_propietario(self):
        if not self.propietario_seleccionado:
            messagebox.showerror("Error","Debe seleccionar un propietario")
            return
        
        if not hasattr(self, 'propietario_seleccionado'):
            messagebox.showerror("Error","Debe seleccionar un propietario")
            return
        
        exito, mensaje = self.controlador.eliminar_propietario(self.propietario_seleccionado.id)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_lista()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)
            
    def limpiar_campos(self):

        self.propietario_seleccionado = None
        self.apellido_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.dni_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.buscar_entry.delete(0, tk.END)
        self.buscar_var.set("")
        self.departamento_entry.delete(0, tk.END)
        self.apellido_entry.focus()

        self.estado_check.config(state=tk.DISABLED)
        self.estado_var.set(False)
        self.boton_crear.config(state=tk.ACTIVE)
