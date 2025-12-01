import mysql.connector
from Modelo.conexion import obtener_conexion
from Modelo.evento import EventoModelo

class EventoControlador:
    def __init__(self):
        self.conectar = obtener_conexion()

    def obtener_eventos(self):
        eventos = []
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT e.id, " \
                           "e.tipo, " \
                           "e.fecha, " \
                           "e.observaciones, " \
                           "e.imagen, " \
                           "e.id_usuario, " \
                           "e.id_propietario, " \
                           "CONCAT(p.Apellido, ' ', p.Nombre) AS NombrePropietario " \
                           "FROM Eventos e " \
                           "JOIN Propietario p ON e.id_propietario = p.id " \
                           "ORDER BY e.fecha DESC"
            cursor.execute(consulta_sql)
            filas = cursor.fetchall()

            for fila in filas:
                evento = EventoModelo(
                    id=fila[0],
                    tipo=fila[1],
                    fecha=fila[2],
                    observaciones=fila[3],
                    imagen=fila[4],
                    id_usuario=fila[5],
                    id_propietario=fila[6],
                    nombrePropietario=fila[7]
                )
                eventos.append(evento)

        except mysql.connector.Error as e:
            print("Error al obtener eventos: ", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return eventos

    def obtener_evento_por_id(self, id_evento):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT e.id, e.tipo, e.fecha, e.observaciones, e.imagen, " \
                           "e.id_usuario, " \
                           "e.id_propietario, " \
                           "CONCAT(p.Apellido, ', ', p.Nombre) AS NombrePropietario " \
                           "FROM Eventos e " \
                           "JOIN Usuario u ON e.id_usuario = u.id " \
                           "JOIN Propietario p ON e.id_propietario = p.id " \
                           "WHERE e.id = %s"
            cursor.execute(consulta_sql, (id_evento,))
            fila = cursor.fetchone()

            # cursor.close()
            # conn.close()

            if fila:
                return EventoModelo(
                    id=fila[0],
                    tipo=fila[1],
                    fecha=fila[2],
                    observaciones=fila[3],
                    imagen=fila[4],
                    id_usuario=fila[5],
                    id_propietario=fila[6],
                    nombrePropietario=fila[7]
                )
            else:
                return None
        except mysql.connector.Error as e:
            print("Error al obtener evento por ID:", e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def nuevo_evento(self, evento : EventoModelo):

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "INSERT INTO Eventos (tipo, observaciones, imagen, id_usuario, id_propietario) " \
                           "VALUES (%s, %s, %s, %s, %s)"
            valores = (
                evento.tipo, 
                evento.observaciones, 
                evento.imagen, 
                evento.id_usuario,
                evento.id_propietario)
            
            cursor.execute(consulta_sql, valores)
            conn.commit()
            return True, "Evento creado correctamente"
        
        except mysql.connector.Error as e:
            return False, f"Error al crear el evento: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def editar_evento(self, evento : EventoModelo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "UPDATE Eventos SET tipo=%s, observaciones=%s, imagen=%s, id_usuario=%s, id_propietario=%s " \
                           "WHERE id=%s"
            valores = (                
                evento.tipo, 
                evento.observaciones, 
                evento.imagen, 
                evento.id_usuario,
                evento.id_propietario,
                evento.id)
            
            cursor.execute(consulta_sql, valores)
            conn.commit()
            return True, "Evento actualizado correctamente"
        
        except mysql.connector.Error as e:
            return False, f"Error al editar el evento: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def obtener_propietarios(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT Id, CONCAT(Apellido, ', ', Nombre)" \
                           "FROM propietario " \
                           "WHERE Estado = True"
            cursor.execute(consulta_sql)
            return cursor.fetchall()
            
        except mysql.connector.Error as e:
            print("Error al obtener Propietarios:", e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()