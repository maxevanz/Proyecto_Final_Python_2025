import re

class ValidadorCampos:

    @staticmethod
    def es_texto_valido(texto, max_len=50):
        return texto.strip() != "" and len(texto.strip()) <= max_len
    
    @staticmethod
    def es_numero(texto):
        return texto.isdigit()
    
    @staticmethod
    def validar_telefono(texto, longitud=10):    
        return texto == "" or (texto.isdigit() and len(texto) <= longitud)

    @staticmethod
    def tiene_longitud_minima(texto, min_len=4):
        return len(texto.strip()) >= min_len
    
    @staticmethod
    def es_rol_valido(rol):
        return rol.lower() in ["admin","usuario","supervisor"]
    
    @staticmethod
    def es_estado_valido(estado):
        return str(estado) in ["1","0","True","False"]
    
    @staticmethod
    def caracteres_permitidos(texto):
        return re.match("^[a-zA-Z0-9_]*$", texto) is not None
    
    @staticmethod
    def validar_usuario(nombre, contraseña, rol, empleado):
        errores = []

        if not ValidadorCampos.es_texto_valido(nombre, 20):
            errores.append("Nombre de usuario inválido.")
        if not ValidadorCampos.tiene_longitud_minima(contraseña, 4):
            errores.append("Contraseña demasiado corta.")
        if not ValidadorCampos.es_rol_valido(rol):
            errores.append("Rol inválido.")
        if not empleado:
            errores.append("Debe vincular un empleado.")
        return errores
    
    @staticmethod
    def validar_empleado(apellido, nombre, telefono):
        errores = []

        if not ValidadorCampos.es_texto_valido(apellido):
            errores.append("Apellido inválido.")
        if not ValidadorCampos.es_texto_valido(nombre):
            errores.append("Nombre inválido.")
        if not ValidadorCampos.validar_telefono(telefono) or len(telefono) != 8:
            errores.append("Telefono inválido. Debe tener 8 dígitos.")
        return errores