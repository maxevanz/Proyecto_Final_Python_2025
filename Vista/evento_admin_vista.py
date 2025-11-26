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
        self.controlador = EventoControlador()
        self.image_path = None
        self.crear_layout()

        self.vista_actual = "admin"


    def crear_layout(self):
        self.columnconfigure(1, weight=1)

        #Formulario
        self.form_frame = tk.LabelFrame(self, text="Agregar Evento")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        tk.Label(self.form_frame, text="Tipo de evento:").grid(row=0, column=0, sticky="w")
        self.tipo_combo = ttk.Combobox(self.form_frame, values=["ingreso", "egreso", "paqueteria", "visitas", "otros"], state="readonly")
        self.tipo_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Propietario:").grid(row=1, column=0, sticky="w")
        self.propietario_combo = ttk.Combobox(self.form_frame, state="readonly")
        self.propietario_combo.grid(row=1, column=1, padx=5, pady=5)
        self.cargar_propietarios()

        tk.Label(self.form_frame, text="Observaciones:").grid(row=2, column=0, sticky="w")
        self.obs_text = tk.Text(self.form_frame, height=4, width=30)
        self.obs_text.grid(row=2, column=1, padx=5, pady=5)

        self.btn_imagen = tk.Button(self.form_frame, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.btn_imagen.grid(row=4, column=0, pady=5)

        self.btn_agregar = tk.Button(self.form_frame, text="Agregar evento", command=self.agregar_evento)
        self.btn_agregar.grid(row=5, column=0, pady=10)

        # Lista de eventos
        lista_frame = tk.LabelFrame(self, text="Eventos registrados")
        lista_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.columnconfigure(1, weight=1)

        self.grilla = ttk.Treeview(lista_frame, columns=("tipo", "fecha", "prop"), show="headings")
        self.grilla.heading("tipo", text="Tipo")
        self.grilla.heading("fecha", text="Fecha")
        self.grilla.heading("prop", text="Propietario")
        self.grilla.pack(fill="both", expand=True)
        self.cargar_eventos()

        self.grilla.bind("<Double-1>", self.ver_evento)

        self.cambiar_frame = tk.LabelFrame(self, text="Cambiar vista")
        self.cambiar_frame.grid(row=1, column=0, padx=10, pady=10)

        self.btn_cambiar_vista = tk.Button(self.cambiar_frame, text="Cambiar Vista", command=self.cambiar_vista)
        self.btn_cambiar_vista.grid(row=0, column=0, pady=10)
        

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes","*.jpg *.png *.jpeg")])
        
        if ruta:
            self.image_path = ruta
            messagebox.showinfo("Imagen seleccionada", ruta)

    def cargar_propietarios(self):
        resultados = self.controlador.obtener_propietarios()
        opciones = [fila[1] for fila in resultados]
        self.mapa_propietarios = {fila[1]: fila[0] for fila in resultados}
        self.propietario_combo['values'] = opciones
        self.propietario_combo.set("")

    def agregar_evento(self):
        tipo = self.tipo_combo.get()
        propietario = self.propietario_combo.get()
        observaciones = self.obs_text.get("1.0", tk.END).strip()
        imagen_evento = self.image_path
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

    def cargar_eventos(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)

        eventos = self.controlador.obtener_eventos()
        for evento in eventos:
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
        self.tipo_combo.set("")
        self.propietario_combo.set("")
        self.obs_text.delete("1.0", "end")

        self.obs_text.focus()

