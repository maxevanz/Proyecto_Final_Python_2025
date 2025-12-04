class ReclamoModelo:
    def __init__(self, id=None, tipo="",fecha=None, mensaje="", foto=None, estado=True, id_usuario=None, nombre_propietario=None):
        self.id = id
        self.tipo = tipo
        self.fecha = fecha
        self.mensaje = mensaje
        self.foto = foto
        self.estado = estado
        self.id_usuario = id_usuario
        self.nombre_propietario = nombre_propietario