import tkinter as tk
from tkinter import Label, Toplevel, ttk,messagebox, filedialog
from PIL import Image, ImageTk
from Modelo.reclamo import ReclamoModelo
from Controlador.reclamoControlador import ReclamoControlador

class VistaReclamos(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)
        self.usuario_actual = usuario_actual
        self.controlador = ReclamoControlador()

        self.crear_formulario()

    def crear_formulario(self):
        self.columnconfigure(1, weight=1)

        #Formulario
        self.form_frame = tk.LabelFrame(self, text="Nuevo Reclamo")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Label(self.form_frame, text="Tipo de reclamo:").grid(row=0, column=0, sticky="e")
        self.tipo_combo = ttk.Combobox(self.form_frame, values=["Portero", "Vecinos", "Edificio", "otros"], state="readonly", width=50)
        self.tipo_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.form_frame, text="Descripcion:").grid(row=1, column=0, sticky="ne")
        self.descrp = tk.Text(self.form_frame, height=4, width=30)
        self.descrp.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.btn_imagen = tk.Button(self.form_frame, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.btn_imagen.grid(row=2, column=0, padx=5, pady=5)
        self.lbl_imagen = tk.Label(self.form_frame, text="Ninguna imagen seleccionada")
        self.lbl_imagen.grid(row=3, column=1, padx=10)

        #Botones
        self.botones = tk.Frame(self)
        self.botones.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.btn_agregar = tk.Button(self.botones, text="Enviar", command="self.nuevo_reclamo")
        self.btn_agregar.grid(row=0, column=1, pady=10)
        self.btn_editar = tk.Button(self.botones, text="Limpiar", command=self.limpiar)
        self.btn_editar.grid(row=1, column=1, pady=10)
        self.btn_limpiar = tk.Button(self.botones, text="Historial de Reclamos", command="self.historial_reclamos")
        self.btn_limpiar.grid(row=3, column=1, pady=10)

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

    def limpiar(self):

        self.tipo_combo.set("")
        self.descrp.delete("1.0", "end")
        self.lbl_imagen.config(text="Ninguna imagen seleccionada")

        self.descrp.focus()

    def nuevo_reclamo(self):
        tipo_reclamo = self.tipo_combo.get()
        descripcion = self.descrp.get("1.0", tk.END).strip()
        imagen_reclamo = self.ruta_imagen
        id_usuario = self.usuario_actual

        if not tipo_reclamo or not descripcion:
            messagebox.showerror("ERROR","Tipo de Reclamo y Descripcion son obligatorios.")
            return
        
        


