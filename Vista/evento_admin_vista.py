import tkinter as tk
from tkinter import ttk,messagebox, filedialog
from PIL import Image, ImageTk
from Modelo.evento import EventoModelo
from Controlador.eventoControlador import EventoControlador

class VistaAdminEvento(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)
        self.usuario_actual = usuario_actual
        self.controlador = EventoControlador()
        self.image_path = None
        self.crear_layout()

    def crear_layout(self):
        self.columnconfigure(1, weight=1)

        #Formulario
        form_frame = tk.LabelFrame(self, text="Agregar Evento")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        tk.Label(form_frame, text="Tipo de evento:").grid(row=0, column=0, sticky="w")
        self.tipo_combo = ttk.Combobox(form_frame, values=["ingreso", "egreso", "paqueteria", "visitas", "otros"])
        self.tipo_combo.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(form_frame, text="Observaciones:").grid(row=2, column=0, sticky="w")
        self.obs_text = tk.Text(form_frame, height=4, width=30)
        self.obs_text.grid(row=3, column=0, padx=5, pady=5)

        self.btn_imagen = tk.Button(form_frame, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.btn_imagen.grid(row=4, column=0, pady=5)

        self.btn_agregar = tk.Button(form_frame, text="Agregar evento", command=self.agregar_evento)
        self.btn_agregar.grid(row=5, column=0, pady=10)

        # Lista de eventos
        lista_frame = tk.LabelFrame(self, text="Eventos registrados")
        lista_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        lista_frame.columnconfigure(0, weight=1)

        self.grilla = ttk.Treeview(lista_frame, columns=("tipo", "fecha", "obs"), show="headings")
        self.grilla.heading("tipo", text="Tipo")
        self.grilla.heading("fecha", text="Fecha")
        self.grilla.heading("obs", text="Observaciones")
        self.grilla.pack(fill="both", expand=True)

        self.grilla.bind("<Double-1>", self.ver_evento)

        cambiar_frame = tk.LabelFrame(self, text="Cambiar vista")
        cambiar_frame.grid(row=1, column=0, padx=10, pady=10)

        self.btn_cambiar_vista = tk.Button(cambiar_frame, text="Cambiar Vista", command="")
        self.btn_cambiar_vista.grid(row=0, column=0, pady=10)

        self.cargar_eventos()

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes","*.jpg *.png *.jpeg")])
        
        if ruta:
            self.image_path = ruta
            messagebox.showinfo("Imagen seleccionada", ruta)

    def agregar_evento(self):
        tipo = self.tipo_combo.get()
        observaciones = self.obs_text.get("1.0", tk.END).strip()
        imagen_evento = self.image_path

        if not tipo:
            messagebox.showerror("Error","Debe seleccionar un tipo evento")
            return
        
        nuevo_evento = EventoModelo(
            tipo= tipo,
            # fecha=None,     #se genera en la base
            observaciones=observaciones,
            imagen= imagen_evento,
            id_usuario=self.usuario_actual
        )

        exito, mensaje = self.controlador.nuevo_evento(nuevo_evento)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def cargar_eventos(self):
        for item in self.grilla.get_children():
            self.grilla.delete(item)

        eventos = self.controlador.obtener_eventos()
        for evento in eventos:
            self.grilla.insert("","end", iid=evento.id, values=(evento.tipo, evento.fecha, evento.observaciones[:40]))

    def ver_evento(self, event):
        item_id = self.grilla.focus()
        evento = self.controlador.obtener_evento_por_id(item_id)
        print(f"este es un mensaje: ", evento)
        if evento:
            detalle = f"Tipo: {evento.tipo}\nFecha: {evento.fecha}\nObservaciones:\n{evento.observaciones}"
            if evento.imagen:
                detalle += f"\nImagen: {evento.imagen}"
            messagebox.showinfo("Detalle deñ evento", detalle)