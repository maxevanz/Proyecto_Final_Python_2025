import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Controlador.eventoControlador import EventoControlador
from Modelo.evento import EventoModelo
from Utilidades.validador_campos import ValidadorCampos

class VistaEvento(tk.Frame):
    def __init__(self, master, id_usuario):
        super().__init__(master)
        self.controlador = EventoControlador()
        self.usuario_actual = id_usuario
        self.imagen_path = None
        
        #Cargar formulario
        self.crear_formulario()


    #Metodos y funciones
    def crear_formulario(self):
        # Tipo de evento
        tk.Label(self, text="Tipo de evento:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo_combo = ttk.Combobox(self, values=["ingreso", "egreso", "paqueteria", "visitas", "otros"])
        self.tipo_combo.grid(row=0, column=1)

        # Observaciones
        tk.Label(self, text="Observaciones:").grid(row=2, column=0, padx=5, pady=5)
        self.obs_text = tk.Text(self, height=4, width=40)
        self.obs_text.grid(row=2, column=1)

        # Imagen
        tk.Label(self, text="Imagen (opcional):").grid(row=3, column=0, padx=5, pady=5)
        self.boton_imagen = tk.Button(self, text="Seleccionar imagen", command=self.seleccionar_imagen)
        self.boton_imagen.grid(row=3, column=1)

        # Botón guardar
        self.boton_guardar = tk.Button(self, text="Guardar evento", command=self.guardar_evento)
        self.boton_guardar.grid(row=5, column=0, columnspan=2, pady=10)

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes","*.png *.jpg *.jpeg *.bmp")]
        )

        if ruta:
            self.imagen_path = ruta
            messagebox.showinfo("Imagen Seleccionada", f"Se seleccionó: \n{ruta}")

    def guardar_evento(self):
        tipo = self.tipo_combo.get()
        fecha = None
        observaciones = self.obs_text.get("1.0", tk.END).strip()
        imagen = self.imagen_path

        errores = ValidadorCampos.validar_evento(tipo, observaciones)
        if errores:
            messagebox.showerror("Errores de validacion", "\n".join(errores))
            return
        
        evento = EventoModelo(
            tipo = tipo,
            fecha = fecha,
            observaciones = observaciones,
            imagen = imagen,
            id_usuario = self.usuario_actual
        )

        exito, mensaje = self.controlador.nuevo_evento(evento)
        if exito:
            messagebox.showinfo("Éxito", mensaje)

        else:
            messagebox.showerror("Error", mensaje)

        # exito, mensaje = self.controlador.crear_usuario(usuario)
        # if exito:
        #     messagebox.showinfo("Éxito", mensaje)
        #     self.limpiar_formulario()
        #     self.cargar_empleados_disponibles()
        #     self.cargar_usuarios()
        # else:
        #     messagebox.showerror("Error", mensaje)
