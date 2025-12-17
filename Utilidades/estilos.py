from tkinter import ttk

def configurar_estilos():
    estilos = ttk.Style()
    estilos.theme_use("clam")       #cambia el tema base

    ################BOTONES###############################################################
    #boton crear (azul)
    estilos.configure("Nuevo.TButton",
                      foreground="white",
                      background="#1E90FF",
                      font=("Arial", 12, "bold"))
    estilos.map("Nuevo.TButton",
                background=[("active","#4682B4"), ("disabled","#A9A9A9")])
    
    #boton editar (verde)
    estilos.configure("Editar.TButton",
                      foreground="white",
                      background="#2E8B57",
                      font=("Arial", 12, "bold"),
                      padding=2)
    estilos.map("Editar.TButton",
                background=[("active","#3CB371"), ("disabled","#A9A9A9")])
    
    #boton eliminar (rojo)
    estilos.configure("Eliminar.TButton",
                      foreground="white",
                      background="#B22222",
                      font=("Arial", 12, "bold"),
                      padding=2)
    estilos.map("Eliminar.TButton",
                background=[("active","#CD5C5C"), ("disabled","#A9A9A9")])
    
    #boton limpiar (gris)
    estilos.configure("Limpiar.TButton",
                      foreground="black",
                      background="#D3D3D3",
                      font=("Arial", 12),
                      padding=2)
    estilos.map("Limpiar.TButton",
                background=[("active","#C0C0C0"), ("disabled","#A9A9A9")])
    
    ###############TREEVIEW################################################################
    estilos.configure("Treeview",
                      font=("Arial", 10),
                      rowheight=25)
    estilos.configure("Treeview.Heading",
                      font=("Arial", 11, "bold"))