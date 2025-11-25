class UsuarioModelo:

    def __init__(self, id = None, nombreusuario="", contraseña="", rol="", estado = True, id_empleado=None, id_propietario=None):
        self.id = id
        self.nombreusuario = nombreusuario
        self.contraseña = contraseña
        self.rol = rol
        self.estado = estado
        self.id_empleado = id_empleado
        self.id_propietario = id_propietario
