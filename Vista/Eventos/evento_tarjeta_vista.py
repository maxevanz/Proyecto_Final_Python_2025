#pip install Pillow

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Controlador.eventoControlador import EventoControlador
from Utilidades.styles.estilos import Estilos
from Utilidades.icon_loader import cargar_icono

#from Vista.evento_admin_vista import VistaAdminEvento

class VistaEventoTarjeta(tk.Frame):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        Estilos.configurar_estilos()
        self.icon_cambiar = cargar_icono("boton-cambiar.png")
        self.icon_zoom = cargar_icono("boton-zoom.png")

        self.usuario_actual = usuario_actual
        self.controlador = EventoControlador()
        self.crear_contenedor_tarjetas()

    
    def crear_contenedor_tarjetas(self):       
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.tarjeta_frame = tk.Frame(canvas)

        self.tarjeta_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0,0), window=self.tarjeta_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_tarjetas()

        self.cambiar_frame = tk.LabelFrame(self, text="Cambiar vista")
        self.cambiar_frame.pack(padx=10, pady=10)

        self.btn_cambiar_vista = ttk.Button(self.cambiar_frame, text="Cambiar Vista", image=self.icon_cambiar, 
                                            compound="right", style="Cambiar.TButton",
                                            command=self.cambiar_vista)
        self.btn_cambiar_vista.pack(pady=10)

    def cargar_tarjetas(self):
        eventos = self.controlador.obtener_eventos()    #<-lista de objetos Evento

        for evento in eventos:
            self.crear_tarjeta(evento)

    def crear_tarjeta(self, evento):
        
        tarjeta = tk.Frame(self.tarjeta_frame, bd=1, relief="solid", padx=10, pady=10)
        tarjeta.pack(pady=5, padx=10, fill="x")

        #Tipo y fecha
        tk.Label(tarjeta, text=f"{evento.tipo.capitalize()} - {evento.fecha}", font=("Arial",12,"bold")).pack(anchor="w")

        #Observaciones
        tk.Label(tarjeta, text=evento.observaciones, font=("Arial",10), wraplength=500, justify="left").pack(anchor="w", pady=5)

        #Botones
        btn_frame = tk.Frame(tarjeta)
        btn_frame.pack(anchor="w", pady=5)
        btn_ver_imagen = ttk.Button(btn_frame, text="Ver imagen", image=self.icon_zoom,
                                    compound="right",
                                    command=lambda: self.ver_imagen(evento))
        btn_ver_imagen.pack(side="left", padx=2)
        #Imagen miniatura
        if evento.imagen:
            try:
                img = Image.open(evento.imagen)
                img.thumbnail((100,100))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(tarjeta, image=img_tk)
                img_label.image = img_tk    #<-mantener referencia
                img_label.pack(anchor="w", pady=5)

            except Exception as e:
                tk.Label(tarjeta, text="Error al cargar la imagen", fg="red").pack(anchor="w")
                btn_ver_imagen.config(state=tk.DISABLED)
        else:
            # Si no hay imagen, también deshabilitar
            btn_ver_imagen.config(state=tk.DISABLED)
                

        

        #tk.Button(btn_frame, text="Ver imagen", command=lambda: self.ver_imagen(evento)).pack(side="left", padx=2)
        
    def ver_imagen(self, evento):
        if evento.imagen:
            top = tk.Toplevel(self)
            top.title("Imagen del evento")
            img = Image.open(evento.imagen)
            img.thumbnail((700, 600))
            img_tk = ImageTk.PhotoImage(img)
            tk.Label(top, image=img_tk).pack()
            top.image = img_tk      #mantener referencia

            # Centrar ventana de detalle con tamaño fijo
            centrar_ventana(top, 500, 400)  # centrar la ventana de detalle
        else:
            messagebox.showinfo("Sin imagen","Este evento no tiene imagen asociada")

    def cambiar_vista(self):
        from Vista.Eventos.evento_admin_vista import VistaAdminEvento
        
        #limpiar el contenido actual
        for vista in self.master.winfo_children():
            vista.destroy()

        vista_seleccionada = VistaAdminEvento(self.master, self.usuario_actual)
        vista_seleccionada.pack(fill=tk.BOTH, expand=True)

def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
