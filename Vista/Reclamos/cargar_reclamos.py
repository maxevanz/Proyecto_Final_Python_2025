from datetime import date
import tkinter as tk
from tkinter import Label, Toplevel, ttk,messagebox, filedialog
from PIL import Image, ImageTk
from fpdf import FPDF
from Modelo.reclamo import ReclamoModelo
from Controlador.reclamoControlador import ReclamoControlador
from Utilidades.PDFs.funciones_para_pdfs import FuncionesParaPDFS
from Utilidades.styles.estilos import Estilos
from Utilidades.icon_loader import cargar_icono


class VistaCargarReclamos(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)
        self.usuario_actual = usuario_actual
        self.controlador = ReclamoControlador()
        self.ruta_imagen = None
        Estilos.configurar_estilos()

        self.crear_formulario()

    def crear_formulario(self):
        self.icon_limpiar = cargar_icono("boton-limpiar.png")
        self.icon_enviar = cargar_icono("boton-enviar.png")
        self.icon_pdf = cargar_icono("boton-pdf.png")
        self.icon_subir = cargar_icono("boton-subir-imagen.png")

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

        self.btn_imagen = ttk.Button(self.form_frame, text="Seleccionar imagen", image=self.icon_subir, 
                                     compound="left",
                                     command=self.seleccionar_imagen)
        self.btn_imagen.grid(row=2, column=0, padx=5, pady=5)
        self.lbl_imagen = tk.Label(self.form_frame, text="Ninguna imagen seleccionada")
        self.lbl_imagen.grid(row=3, column=1, padx=10)

        #Botones
        self.botones = tk.Frame(self)
        self.botones.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.btn_agregar = ttk.Button(self.botones, text="Enviar", image=self.icon_enviar, 
                                      compound="right", style="Enviar.TButton",
                                      command=self.nuevo_reclamo)
        self.btn_agregar.grid(row=0, column=1, pady=10)
        self.btn_editar = ttk.Button(self.botones, text="Limpiar", image=self.icon_limpiar, 
                                     compound="right", style="Limpiar.TButton",
                                     command=self.limpiar)
        self.btn_editar.grid(row=1, column=1, pady=10)
        self.btn_limpiar = ttk.Button(self.botones, text="Historial de Reclamos", image=self.icon_pdf, 
                                      compound="right", style="PDF.TButton",
                                      command=self.generar_pdf_por_propietario)
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
        
        reclamo = ReclamoModelo(
            tipo=tipo_reclamo,
            mensaje=descripcion,
            foto=imagen_reclamo,
            id_usuario=id_usuario
        )
        
        exito, mensaje = self.controlador.nuevo_reclamo(reclamo)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar()
        else:
            messagebox.showerror("ERROR", mensaje)
        
    def generar_pdf_por_propietario(self):
        reclamos = self.controlador.obtener_reclamos_por_usuario(self.usuario_actual)

        if not reclamos:
            messagebox.showinfo("Atención", "Aún no generó ningun reclamo.")
            return
        
        #Ventana para elegir ubicacion y nombre
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Reporte_{date.today().strftime('%Y-%m-%d')}.pdf",
            title="Guardar como"
        )

        if not nombre_archivo:  #Si el usuario cancela
            print("Exportacion cancelada")
            return        

        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Lista de Reclamos", ln=True, align="C")
        pdf.ln(5)

        # Encabezados
        pdf.set_font("Arial", 'B', 10)        
        anchos  = [50, 25, 50, 100, 30]
        alto_linea = 7
        headers = ["Propietario", "Tipo", "Fecha", "Mensaje", "Estado"]

        x_ini = pdf.get_x()
        y_ini = pdf.get_y()
        x = x_ini

        for i, h in enumerate(headers):
            pdf.rect(x, y_ini, anchos[i], alto_linea + 3)
            pdf.set_xy(x, y_ini)
            pdf.cell(anchos[i], alto_linea + 3, h, 0, 0, "C")
            x += anchos[i]
        pdf.set_xy(x_ini, y_ini + alto_linea + 3)

        # Cuerpo
        pdf.set_font("Arial", size=10)
        pdf.set_font("Arial", size=10)
        for reclamo in reclamos:
            propietario = reclamo.nombre_propietario
            tipo = reclamo.tipo 
            fecha = str(reclamo.fecha) 
            mensaje = reclamo.mensaje 
            estado = "Pendiente" if reclamo.estado == 1 else "Revisado"

            FuncionesParaPDFS.dibujar_fila(pdf, [str(propietario), str(tipo), str(fecha), str(mensaje), str(estado)], anchos, alto_linea)

        #Guardar archivo
        pdf.output(nombre_archivo)
        print(f"PDF generado: reclamos_propietario_{self.usuario_actual}.pdf")

    def historial_reclamos(self):
        pass


