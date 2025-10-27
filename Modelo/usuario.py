from .conexion import obtener_conexion

class UsuarioModelo:

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