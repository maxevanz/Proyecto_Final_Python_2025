from .conexion import obtener_conexion

class UsuarioModelo:

<<<<<<< HEAD
    def __init__(self, id = None, nombreusuario="", contraseña="", rol="", estado = True, id_empleado=None):
        self.id = id
        self.nombreusuario = nombreusuario
        self.contraseña = contraseña
        self.rol = rol
        self.estado = estado
        self.id_empleado = id_empleado
=======
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def obtener_usuario(username, password):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM Usuario WHERE NombreUsuario = %s AND Contraseña = %s AND Estado = TRUE"
            cursor.execute(query, (username, password))
            resultado = cursor.fetchone()
    
            return resultado
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
>>>>>>> 6d8a6ddd699659abea0c6836ca7d6adc65ddb472
