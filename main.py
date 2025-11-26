import tkinter as tk
from Vista.login import LoginFrame
from Vista.pantalla_principal import PantallaPrincipalFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Portería")

        self.login_frame = LoginFrame(self, self.mostrar_pantalla_principal)
        self.pantalla_principal_frame = PantallaPrincipalFrame(self, self.mostrar_login)

        self.geometry("300x500")
        
        self.login_frame.pack()

    def mostrar_login(self):
        self.pantalla_principal_frame.pack_forget()
        self.geometry("300x500")
        self.login_frame.pack()
        self.config(menu=None)          #oculta el menu al cerrar sesion

    def mostrar_pantalla_principal(self, id_usuario, nombre_usuario, rol):
        self.login_frame.pack_forget()
        self.geometry("800x600")
        self.pantalla_principal_frame.set_usuario(id_usuario, nombre_usuario, rol)
        self.pantalla_principal_frame.mostrar_menu()

if __name__ == "__main__":
    app = App()
    app.mainloop()