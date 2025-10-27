from .conexion import obtener_conexion

class EventoModelo:
    def registrar_evento(tipo, observaciones, id_usuario):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            query = "INSERT INTO Eventos(tipo, observaciones, id_usuario) VALUES(%s, %s, %s)"
            cursor.execute(query, (tipo, observaciones, id_usuario))
            conn.commit()
    
        except Exception as e:
            print(f"Error al registrar el evento: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

