from Modelo.usuario import UsuarioModelo

class UsuarioControlador:
    def verificar_credeciales(self, username, password):
        usuario = UsuarioModelo.obtener_usuario(username, password)
        return usuario