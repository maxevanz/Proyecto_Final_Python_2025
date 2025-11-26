
class EventoModelo:
    def __init__(self, id=None, tipo="", fecha=None, observaciones="", imagen=None, id_usuario=None, id_propietario=None, nombrePropietario=None):
        self.id = id
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones
        self.imagen = imagen
        self.id_usuario = id_usuario
        self.id_propietario = id_propietario
        self.nombre_propietario = nombrePropietario

