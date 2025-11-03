#pip install Pillow

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Controlador.eventoControlador import EventoControlador

class VistaEventoTarjeta(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)
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
                tk.Label(tarjeta, text="Error al cargar imagen", fg="red").pack(anchor="w")

        #Botones
        btn_frame = tk.Frame(tarjeta)
        btn_frame.pack(anchor="w", pady=5)
        
        tk.Button(btn_frame, text="Ver imagen", command=lambda: self.ver_imagen(evento)).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Editar", command=lambda: self.editar_evento(evento)).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Eliminar", command=lambda: self.eliminar_evento(evento)).pack(side="left", padx=2)


    def ver_imagen(self, evento):
        if evento.imagen:
            top = tk.Toplevel(self)
            top.title("Imagen del evento")
            img = Image.open(evento.imagen)
            img_tk = ImageTk.PhotoImage(img)
            tk.Label(top, image=img_tk).pack()
            top.image = img_tk      #mantener referencia
        else:
            messagebox.showinfo("Sin imagen","Este evento no tiene imagen asociada")

    def editar_evento(self, evento):
        messagebox.showinfo("Editar",f"Editar evento ID {evento.id}")

    def eliminar_evento(self, evento):
        confirm = messagebox.askyesno("Eliminar",f"¿Eliminar evento ID {evento.id}?")
        if confirm:
            if self.controlador.eliminar_evento(evento.id):
                messagebox.showinfo("Eliminado","Evento eliminado correctamente")
                for widget in self.tarjeta_frame.winfo_children():
                    widget.destroy()
                self.cargar_tarjetas()
            else:
                messagebox.showerror("Error","No se pudo eliminar el evento")

