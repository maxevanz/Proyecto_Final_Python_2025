import tkinter as tk
from tkinter import Label, Toplevel, ttk,messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from Modelo.reclamo import ReclamoModelo
from Controlador.reclamoControlador import ReclamoControlador
from Utilidades.PDFs.funciones_para_pdfs import FuncionesParaPDFS
from datetime import date
from fpdf import FPDF

class VistaVerReclamos(tk.Frame):
    def __init__(self, master=None, usuario_actual=None):
        super().__init__(master)
        self.usuario_actual = usuario_actual
        self.controlador = ReclamoControlador()

        self.crear_formulario_busqueda()
        self.mostrar_grilla()

    def crear_formulario_busqueda(self):

        tk.Label(self, text="Administrar Reclamos", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="nw")

        ###contenedor filtrar###
        self.filtro_frame = tk.LabelFrame(self, text="Filtrar")
        self.filtro_frame.grid(row=1, column=0,  sticky="w", padx=5, pady=5)
        self.filtro_frame.columnconfigure(0, weight=1)

        ###propietario###
        self.propietario = tk.Frame(self.filtro_frame)
        self.propietario.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        # Permitir que la columna 1 (donde está el combo) se expanda
        self.propietario.columnconfigure(1, weight=1)

        tk.Label(self.propietario, text="Propietario:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.propietario_combo = ttk.Combobox(self.propietario, state="readonly")
        self.propietario_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")        
        self.cargar_propietarios()
        self.propietario_combo.current(0)
        
        # Vincular reclamo al cambio de propietario
        #self.propietario_combo.bind("<<ComboboxSelected>>", self.actualizar_grilla)  #actualiza dinamicamente la grilla cuando cambia el propietario

        ###desde hasta###
        self.fechas_frame = tk.Frame(self.filtro_frame)
        self.fechas_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        #self.fechas.columnconfigure(1, weight=1)

        tk.Label(self.fechas_frame, text="Desde: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fecha_inicio = DateEntry(self.fechas_frame, width=12, background='darkblue'
                                      , foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
                                      , state="readonly", year=2025, month=1, day=1)
        self.fecha_inicio.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.fechas_frame, text="Hasta:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.fecha_fin = DateEntry(self.fechas_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
                                   , state="readonly", maxdate=date.today())   # no permite elegir más allá de hoy)
        self.fecha_fin.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.boton_filtrar = tk.Button(self.fechas_frame, text="Filtrar", command=self.filtrar_campos)
        self.boton_filtrar.grid(row=1, column=4, padx=10, pady=5, sticky="w")

        ##estado###
        self.estado_frame = tk.Frame(self.filtro_frame)
        self.estado_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.estado_frame.columnconfigure(1, weight=1)

        tk.Label(self.estado_frame, text="Estado: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.estado_combo = ttk.Combobox(self.estado_frame, values=["Todos","Pendiente","Revisado"], state="readonly")
        self.estado_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.estado_combo.current(0)    #Selecciona por defecto Todos

        ###contenedor Busqueda###
        self.busqueda_frame = tk.Frame(self)
        self.busqueda_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.busqueda_frame.columnconfigure(1, weight=1)

        tk.Label(self.busqueda_frame, text="Buscar: ").grid(row=0, column=0, sticky="w", padx=5)
        self.buscar_var = tk.StringVar()
        self.buscar_entry = tk.Entry(self.busqueda_frame, textvariable=self.buscar_var)
        self.buscar_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        self.buscar_var.trace_add("write", self.filtrar_por_busqueda)

        ###Contenedor Botones###
        self.botones_frame = tk.LabelFrame(self, text="Acciones")
        self.botones_frame.grid(row=1, column=1,  sticky="e", padx=5, pady=5)
        self.botones_frame.columnconfigure(0, weight=1)

        self.boton_limpiar_campos = tk.Button(self.botones_frame, text="Limpiar Campos", command=self.limpiar)
        self.boton_limpiar_campos.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.boton_generar_pdf = tk.Button(self.botones_frame, text="Exportar a PDF", command=self.exportar_pdf)
        self.boton_generar_pdf.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.boton_generar_excel = tk.Button(self.botones_frame, text="Exportar a Excel")
        self.boton_generar_excel.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def mostrar_grilla(self):
        #Lista de Reclamos

        self.grilla = ttk.Treeview(self, columns=("Propietario", "Tipo", "Fecha", "Mensaje", "Estado"), show="headings")
        self.grilla.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for col in ("Propietario", "Tipo", "Fecha", "Mensaje", "Estado"):
            self.grilla.heading(col, text=col)
            self.grilla.column(col, width=100)       

        self.grilla.bind("<<TreeviewSelect>>", "self.seleccionar_evento")
        self.grilla.bind("<Double-1>", self.ver_reclamo)
        self.cargar_reclamos()

    def actualizar_grilla(self, event=None):
        # Obtener el valor seleccionado en el combo
        propietario_seleccionado = self.propietario_combo.get()        

        # Si seleccionó "Todos", traemos todos los reclamos
        if propietario_seleccionado == "Todos":
            reclamos = self.controlador.obtener_reclamos()
        else:
            id_propietario = self.mapa_propietarios[propietario_seleccionado]
            reclamos = self.controlador.obtener_reclamos_por_propietario(id_propietario)

        # Limpiar la grilla
        for item in self.grilla.get_children():
            self.grilla.delete(item)

        # Insertar los reclamos filtrados
        for reclamo in reclamos:
            tag = "Pendiente" if reclamo.estado == 1 else "Revisado"
            estado_texto = "Pendiente" if reclamo.estado == 1 else "Revisado"
            self.grilla.insert(
                "",
                tk.END,
                iid=reclamo.id,
                values=(reclamo.nombre_propietario, reclamo.tipo, reclamo.fecha, estado_texto),
                tags=(tag,)
            )

    def cargar_propietarios(self):
        resultados = self.controlador.obtener_propietarios()
        opciones = [f"{fila[1]}" for fila in resultados]  # o Apellido + Nombre
        self.mapa_propietarios = {f"{fila[1]}": fila[0] for fila in resultados}

        #Agregar "Todos" al inicio
        opciones.insert(0, "Todos")

        self.propietario_combo['values'] = opciones
        self.propietario_combo.current(0)       #Seleccionar "Todos" por defecto

    def cargar_reclamos(self):
        self.grilla.tag_configure("Pendiente", background="#f2dede")  # rojo claro
        self.grilla.tag_configure("Revisado", background="#d4edda")  # verde claro

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        self.reclamos = self.controlador.obtener_reclamos()
        for reclamo in self.reclamos:
            tag = "Pendiente" if reclamo.estado == 1 else "Revisado"
            estado_texto = "Revisado" if reclamo.estado == 0 else "Pendiente"
            self.grilla.insert(
                "",
                tk.END, 
                iid=reclamo.id, 
                values=(reclamo.nombre_propietario, reclamo.tipo, reclamo.fecha, reclamo.mensaje, estado_texto),
                tags=(tag,))
  
    def ver_reclamo(self, event):
        # Si ya hay una ventana abierta, no crear otra
        if hasattr(self, "detalle_win") and self.detalle_win is not None and self.detalle_win.winfo_exists():
            self.detalle_win.lift()  # traer al frente si ya existe
            return

        item_id = self.grilla.focus()
        reclamo = self.controlador.obtener_reclamo_por_id(item_id)

        if reclamo:
            # Crear ventana de detalle
            self.detalle_win = tk.Toplevel(self)
            self.detalle_win.title("Detalle del reclamo")
            self.detalle_win.resizable(False, False)

            # Centrar ventana de detalle con tamaño fijo
            centrar_ventana(self.detalle_win, 500, 400)  # centrar la ventana de detalle

            # Cuando se cierre, eliminar referencia
            self.detalle_win.protocol("WM_DELETE_WINDOW", self.cerrar_detalle)

            # Texto descriptivo
            detalle_texto = ( 
                f"Tipo: {reclamo.tipo}\n"
                f"Fecha: {reclamo.fecha}\n"
                f"Propietario: {reclamo.nombre_propietario}\n"
                f"Mensaje:\n{reclamo.mensaje}")
            tk.Label(self.detalle_win, text=detalle_texto, justify="left").pack(padx=10, pady=10)

            # Imagen (si existe)
            if reclamo.foto:
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(reclamo.foto)
                    img = img.resize((300, 200))
                    foto = ImageTk.PhotoImage(img)

                    lbl_img = tk.Label(self.detalle_win, image=foto)
                    lbl_img.image = foto  # mantener referencia
                    lbl_img.pack(padx=10, pady=10)
                except Exception as e:
                    tk.Label(self.detalle_win, text=f"No se pudo cargar la imagen: {e}").pack(padx=10, pady=10)
            if reclamo.estado == 1:
                tk.Button(self.detalle_win, text="Revisado", command=self.cambiar_estado, state=tk.ACTIVE).pack(padx=10, pady=10)                
            else:
                tk.Button(self.detalle_win, text="Revisado", command=self.cambiar_estado, state=tk.DISABLED).pack(padx=10, pady=10)

    def cambiar_estado(self):
        item_id = self.grilla.focus()
        reclamo = self.controlador.obtener_reclamo_por_id(item_id)

        exito, mensaje = self.controlador.cambiar_estado(item_id)

        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.cargar_reclamos()
            self.limpiar()
            self.cerrar_detalle()
        else:
            messagebox.showerror()

    def cerrar_detalle(self):
        # destruir ventana y limpiar referencia
        self.detalle_win.destroy()
        self.detalle_win = None

    def filtrar_por_busqueda(self, *args):
        texto = self.buscar_var.get().lower()

        for item in self.grilla.get_children():
            self.grilla.delete(item)

        for reclamo in self.reclamos:
            tag = "Pendiente" if reclamo.estado == 1 else "Revisado"
            estado_texto = "Revisado" if reclamo.estado == 0 else "Pendiente"
            # estado_legible = "Activo" if str(reclamo.estado) == "1" else "Inactivo"
            # tag = "estado0" if str(reclamo.estado) == "0" else ""

            #Convertir todos los campos a texto y buscar coincidencias
            valores = f"{reclamo.nombre_propietario} {reclamo.tipo} {reclamo.fecha} {reclamo.mensaje} {estado_texto}".lower()
            if texto in valores:
                self.grilla.insert(
                    "",tk.END,
                    values=(reclamo.nombre_propietario, reclamo.tipo, reclamo.fecha, reclamo.mensaje, estado_texto),
                    tags=(tag,)
                )

    def filtrar_campos(self):
        #Obtener valores de los filtros
        propietario = self.propietario_combo.get()
        estado = self.estado_combo.get()
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()

        #Armar consulta dinamica en el controlador
        reclamos = self.controlador.obtener_reclamos_filtrados(
            propietario = propietario,
            estado = estado,
            fecha_inicio = fecha_inicio,
            fecha_fin = fecha_fin
        )

        #limpiar la grilla
        for item in self.grilla.get_children():
            self.grilla.delete(item)
        
        #Insertar reclamos filtrados
        for reclamo in reclamos:
            id = reclamo[0]
            fecha = reclamo[1]
            tipo = reclamo[2]
            mensaje = reclamo[3]
            foto = reclamo[4]
            estado = reclamo[5]
            propietario = reclamo[6]

            tag = "Pendiente" if estado == 1 else "Revisado"
            estado_texto = "Pendiente" if estado == 1 else "Revisado"

            self.grilla.insert(
                "",
                tk.END,
                iid=id,
                values=(propietario, tipo, fecha, mensaje, estado_texto),
                tags=(tag,)
            )

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

    def generar_pdf(self, reclamos, fecha_inicio=None, fecha_fin=None):
        # Nombre sugerido dinámico
        if fecha_inicio and fecha_fin:
            nombre_sugerido = f"reclamos_{fecha_inicio.strftime('%Y-%m-%d')}_a_{fecha_fin.strftime('%Y-%m-%d')}.pdf"
        elif fecha_inicio:
            nombre_sugerido = f"reclamos_{fecha_inicio.strftime('%Y-%m-%d')}.pdf"
        else:
            nombre_sugerido = f"reclamos_{date.today().strftime('%Y-%m-%d')}.pdf"

        #Ventana para elegir ubicacion y nombre
        nombre_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=nombre_sugerido,
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
        pdf.ln(2)

        # Encabezados
        pdf.set_font("Arial", 'B', 10)
        anchos = [50, 25, 50, 100, 30]  # ajustá según tu diseño
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
        for fila in reclamos:
            propietario, tipo, fecha, mensaje, estado = fila
            FuncionesParaPDFS.dibujar_fila(pdf, [propietario, tipo, fecha, mensaje, estado], anchos, alto_linea)
        #Guardar archivo
        pdf.output(nombre_archivo)
        print(f"PDF generado: {nombre_archivo}")

    def exportar_pdf(self):
        propietario = self.propietario_combo.get()
        estado = self.estado_combo.get()
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()

        #Obtener los datos directamente de la grilla
        reclamos = []
        for item in self.grilla.get_children():
            valores = self.grilla.item(item, "values")
            reclamos.append(valores)

        if reclamos:
            self.generar_pdf(reclamos, fecha_inicio, fecha_fin)
        else:
            print("No hay reclamos en la grilla para exportar.")

    def limpiar(self):
        self.buscar_entry.delete(0, tk.END)
        self.propietario_combo.set("")
        self.propietario_combo.current(0)

        self.fecha_inicio.set_date('2025-01-01')
        self.fecha_fin.set_date(date.today())

        self.estado_combo.set("")
        self.estado_combo.current(0)
        
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (ancho // 2)
    y = (screen_height // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


