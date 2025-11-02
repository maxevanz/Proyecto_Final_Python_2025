class EmpleadoModelo:

    def __init__(self, apellido, nombre, correo, telefono, estado, id=None):
        self.id = id
        self.apellido = apellido
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.estado = estado
