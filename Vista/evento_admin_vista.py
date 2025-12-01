import tkinter as tk
from tkinter import Label, Toplevel, ttk,messagebox, filedialog
from PIL import Image, ImageTk
from Modelo.evento import EventoModelo
from Controlador.eventoControlador import EventoControlador

#from Vista.evento_tarjeta_vista import VistaEventoTarjeta

class VistaAdminEvento(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)

        self.usuario_actual = usuario_actual
        self.evento_seleccionado = None

        self.controlador = EventoControlador()
        self.image_path = None
        self.crear_layout()

        self.vista_actual = "admin"


    def crear_layout(self):
        self.columnconfigure(1, weight=1)

        #Formulario
        self.form_frame = tk.LabelFrame(self, text="Agregar Evento")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Label(self.form_frame, text="Tipo de evento:").grid(row=0, column=0, sticky="e")
        self.tipo_combo = ttk.Combobox(self.form_frame, values=["ingreso", "egreso", "paqueteria", "visitas", "otros"], state="readonly", width=50)
        self.tipo_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.form_frame, text="Propietario:").grid(row=1, column=0, sticky="e")
        self.propietario_combo = ttk.Combobox(self.form_frame, state="readonly", width=50)
        self.propietario_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.cargar_propietarios()

        tk.Label(self.form_frame, text="Observaciones:").grid(row=2, column=0, sticky="ne")
        self.obs_text = tk.Text(self.form_frame, height=4, width=30)
        self.obs_text.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.btn_imagen = tk.Button(self.form_frame, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.btn_imagen.grid(row=4, column=0, padx=5, pady=5)
        self.lbl_imagen = tk.Label(self.form_frame, text="Ninguna imagen seleccionada")
        self.lbl_imagen.grid(row=4, column=1, padx=10)

        #Botones
        self.botones = tk.Frame(self)
        self.botones.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.btn_agregar = tk.Button(self.botones, text="Agregar evento", command=self.agregar_evento)
        self.btn_agregar.grid(row=0, column=1, pady=10)
        self.btn_editar = tk.Button(self.botones, text="Editar evento", command=self.editar_evento)
        self.btn_editar.grid(row=1, column=1, pady=10)
        self.btn_limpiar = tk.Button(self.botones, text="Limpiar", command=self.limpiar)
        self.btn_limpiar.grid(row=2, column=1, pady=10)
        self.btn_cambiar_vista = tk.Button(self.botones, text="Cambiar Vista", command=self.cambiar_vista)
        self.btn_cambiar_vista.grid(row=3, column=1, pady=10)

        #Lista de Eventos
        self.grilla = ttk.Treeview(self, columns=("Tipo", "Fecha", "Propietario"), show="headings")
        self.grilla.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for col in ("Tipo","Fecha","Propietario"):
            self.grilla.heading(col, text=col)
            self.grilla.column(col, width=100)       

        self.grilla.bind("<<TreeviewSelect>>", self.seleccionar_evento)
        self.grilla.bind("<Double-1>", self.ver_evento)
        self.cargar_eventos()

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes","*.jpg *.png *.jpeg")])
        
        if ruta:
            # Mostrar solo el nombre del archivo
            import os
            nombre = os.path.basename(ruta)
            self.lbl_imagen.config(text=f"Seleccionada: {nombre}")
            # Guardar ruta si la necesitás
            self.ruta_imagen = ruta
            messagebox.showinfo("Imagen seleccionada", ruta)

    def seleccionar_evento(self, event):
        seleccion = self.grilla.focus()        
        self.btn_agregar.config(state = tk.DISABLED)

        if seleccion:
            item = seleccion
            self.evento_seleccionado = self.controlador.obtener_evento_por_id(item)

            self.tipo_combo.set(self.evento_seleccionado.tipo)
            self.propietario_combo.set(self.evento_seleccionado.nombre_propietario)
            self.obs_text.delete("1.0","end")
            self.obs_text.insert("1.0", self.evento_seleccionado.observaciones)
            # Mostrar la ruta de la imagen en el Label
            if self.evento_seleccionado.imagen:
                self.lbl_imagen.config(text="")
                self.lbl_imagen.config(text=f"{self.evento_seleccionado.imagen}")
            else:
                self.lbl_imagen.config(text="Sin imagen asociada")
                self.ruta_imagen = "Sin imagen asociada"
        
    def cargar_propietarios(self):
        resultados = self.controlador.obtener_propietarios()
        opciones = [f"{fila[1]}" for fila in resultados]  # o Apellido + Nombre
        self.mapa_propietarios = {f"{fila[1]}": fila[0] for fila in resultados}
        self.propietario_combo['values'] = opciones

        self.propietario_combo.set("")

    def agregar_evento(self):
        tipo = self.tipo_combo.get()
        propietario = self.propietario_combo.get()
        observaciones = self.obs_text.get("1.0", tk.END).strip()
        imagen_evento = self.ruta_imagen
        id_usuario = self.usuario_actual


        if not tipo or not propietario:
            messagebox.showerror("Error","Debe seleccionar un tipo evento y propietario")
            return
        
        id_propietario = self.mapa_propietarios[propietario]
        
        nuevo_evento = EventoModelo(
            tipo= tipo,
            # fecha=None,     #se genera en la base
            observaciones=observaciones,
            imagen= imagen_evento,
            id_usuario=id_usuario,
            id_propietario = id_propietario
        )

        exito, mensaje = self.controlador.nuevo_evento(nuevo_evento)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar()
            self.cargar_eventos()
        else:
            messagebox.showerror("Error", mensaje)

    def editar_evento(self):
        if not self.evento_seleccionado:
            messagebox.showerror("Advertencia","Debe seleccionar un evento")
            return
        
        propietario = self.propietario_combo.get()
        id_propietario = self.mapa_propietarios[propietario]
        imagen = self.lbl_imagen.cget("text")

        if id_propietario is None:
            messagebox.showerror("Error", f"Propietario '{propietario}' no encontrado en el mapa")
            return
        #Validacion
        evento = EventoModelo(
            id=self.evento_seleccionado.id,
            tipo=self.tipo_combo.get(),
            observaciones=self.obs_text.get("1.0", "end-1c"),  # obtiene el contenido del Text
            imagen=imagen,
            id_usuario=self.usuario_actual,
            id_propietario=id_propietario
        )

        exito, mensaje = self.controlador.editar_evento(evento)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar()
            self.cargar_eventos()
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_eventos(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)

        self.eventos = self.controlador.obtener_eventos()
        for evento in self.eventos:
            self.grilla.insert(
                "",
                tk.END, 
                iid=evento.id, 
                values=(evento.tipo, evento.fecha , evento.nombre_propietario))

    def ver_evento(self, event):
        # Si ya hay una ventana abierta, no crear otra
        if hasattr(self, "detalle_win") and self.detalle_win is not None and self.detalle_win.winfo_exists():
            self.detalle_win.lift()  # traer al frente si ya existe
            return

        item_id = self.grilla.focus()
        evento = self.controlador.obtener_evento_por_id(item_id)

        if evento:
            # Crear ventana de detalle
            self.detalle_win = tk.Toplevel(self)
            self.detalle_win.title("Detalle del evento")
            self.detalle_win.resizable(False, False)

            # Centrar ventana de detalle con tamaño fijo
            centrar_ventana(self.detalle_win, 500, 400)  # centrar la ventana de detalle

            # Cuando se cierre, eliminar referencia
            self.detalle_win.protocol("WM_DELETE_WINDOW", self.cerrar_detalle)

            # Texto descriptivo
            detalle_texto = ( 
                f"Tipo: {evento.tipo}\n"
                f"Fecha: {evento.fecha}\n"
                f"Propietario: {evento.nombre_propietario}\n"
                f"Observaciones:\n{evento.observaciones}")
            tk.Label(self.detalle_win, text=detalle_texto, justify="left").pack(padx=10, pady=10)

            # Imagen (si existe)
            if evento.imagen:
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(evento.imagen)
                    img = img.resize((300, 200))
                    foto = ImageTk.PhotoImage(img)

                    lbl_img = tk.Label(self.detalle_win, image=foto)
                    lbl_img.image = foto  # mantener referencia
                    lbl_img.pack(padx=10, pady=10)
                except Exception as e:
                    tk.Label(self.detalle_win, text=f"No se pudo cargar la imagen: {e}").pack(padx=10, pady=10)

    def cerrar_detalle(self):
        # destruir ventana y limpiar referencia
        self.detalle_win.destroy()
        self.detalle_win = None

    def cambiar_vista(self):
        from Vista.evento_tarjeta_vista import VistaEventoTarjeta
        
        #limpiar el contenido actual
        for vista in self.master.winfo_children():
            vista.destroy()

        vista_seleccionada = VistaEventoTarjeta(self.master, self.usuario_actual)
        vista_seleccionada.pack(fill=tk.BOTH, expand=True)
        
        # #alternar entre vistas
        # if self.vista_actual == "admin":
        #     vista_seleccionada = VistaEventoTarjeta(self.master, self.usuario_actual)
        #     self.vista_actual = "tarjeta"

        # else:
        #     vista_seleccionada = VistaAdminEvento(self.master)
        #     self.vista_actual = "admin"

        # vista_seleccionada.pack(fill=tk.BOTH, expand=True)

    def limpiar(self):

        self.btn_agregar.config(state=tk.ACTIVE)
        self.evento_seleccionado = None
        self.tipo_combo.set("")
        self.propietario_combo.set("")
        self.obs_text.delete("1.0", "end")
        self.lbl_imagen.config(text="Ninguna imagen seleccionada")

        self.obs_text.focus()

def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
