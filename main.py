import tkinter as tk
from Vista.login import LoginFrame
from Vista.pantalla_principal import PantallaPrincipalFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Portería")

        self.login_frame = LoginFrame(self, self.mostrar_pantalla_principal)
        self.pantalla_principal_frame = PantallaPrincipalFrame(self, self.mostrar_login)

        #self.geometry("300x500")
        self.centrar_ventana(300, 500)   # login centrado
        self.resizable(False, False)
        
        self.login_frame.pack()

    def mostrar_login(self):
        self.pantalla_principal_frame.pack_forget()
        #self.geometry("300x500")
        self.centrar_ventana( 300, 500)   # login centrado
        self.login_frame.pack()
        self.config(menu=None)          #oculta el menu al cerrar sesion

    def mostrar_pantalla_principal(self, id_usuario, nombre_usuario, rol):
        self.login_frame.pack_forget()
        #self.geometry("800x600")
        self.centrar_ventana(800, 600)   # login centrado
        self.pantalla_principal_frame.set_usuario(id_usuario, nombre_usuario, rol)
        self.pantalla_principal_frame.mostrar_menu()

    def centrar_ventana(self, ancho, alto):
        # obtener tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calcular coordenadas para centrar
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)

        # aplicar geometría
        self.geometry(f"{ancho}x{alto}+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.mainloop()