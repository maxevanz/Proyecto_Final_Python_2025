import mysql.connector
from Modelo.conexion import obtener_conexion
from Modelo.reclamo import ReclamoModelo

class ReclamoControlador:
    def __init__(self):
        self.conectar = obtener_conexion()

    def nuevo_reclamo(self, reclamo : ReclamoModelo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "INSERT INTO Reclamo (tipo, mensaje, foto, id_usuario) " \
                           "VALUES (%s, %s, %s, %s)"
            valores = (
                reclamo.tipo,
                reclamo.mensaje,
                reclamo.foto,
                reclamo.id_usuario
            )

            cursor.execute(consulta_sql, valores)
            conn.commit()
            return True, "Reclamo creado correctamente"
        
        except mysql.connector.Error as e:
            return False, f"Error al crear el reclamo: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
     
    def obtener_reclamos(self):
        reclamos = []
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT r.id, " \
                           "r.tipo, " \
                           "r.fecha, " \
                           "r.mensaje, " \
                           "r.foto, " \
                           "r.estado, " \
                           "r.id_usuario, " \
                           "CONCAT(p.Apellido, ' ', p.Nombre) AS Propietario " \
                           "FROM Reclamo r " \
                           "LEFT JOIN Usuario u ON r.id_usuario = u.id " \
                           "LEFT JOIN Propietario p ON u.id_propietario = p.id " \
                           "ORDER BY r.fecha DESC"
            
            cursor.execute(consulta_sql)
            filas = cursor.fetchall()

            for fila in filas:
                reclamo = ReclamoModelo(
                    id=fila[0],
                    tipo=fila[1],
                    fecha=fila[2],
                    mensaje=fila[3],
                    foto=fila[4],
                    estado=fila[5],
                    id_usuario=fila[6],
                    nombrePropietario=fila[7]
                )
                reclamos.append(reclamo)

        except mysql.connector.Error as e:
            print("Error al obtener reclamos: ", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return reclamos

    def obtener_reclamo_por_id(self, id_reclamo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT r.id, " \
                           "r.tipo, " \
                           "r.fecha, " \
                           "r.mensaje, " \
                           "r.foto, " \
                           "r.estado, " \
                           "r.id_usuario, " \
                           "CONCAT(p.Apellido, ' ', p.Nombre) AS Propietario " \
                           "FROM Reclamo r " \
                           "LEFT JOIN Usuario u ON r.id_usuario = u.id " \
                           "LEFT JOIN Propietario p ON u.id_propietario = p.id " \
                           "WHERE r.id = %s " \
                           "ORDER BY r.fecha DESC"
                           
            cursor.execute(consulta_sql, (id_reclamo,))
            fila = cursor.fetchone()

            if fila:
                return ReclamoModelo(
                    id=fila[0],
                    tipo=fila[1],
                    fecha=fila[2],
                    mensaje=fila[3],
                    foto=fila[4],
                    estado=fila[5],
                    id_usuario=fila[6],
                    nombrePropietario=fila[7]
                )
            else:
                return None
        except mysql.connector.Error as e:
            print("Error al obtener reclamo por ID:", e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_reclamos_por_propietario(self, id_propietario):
        reclamos = []
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT r.id, " \
                           "r.tipo, " \
                           "r.fecha, " \
                           "r.mensaje, " \
                           "r.foto, " \
                           "r.estado, " \
                           "r.id_usuario, " \
                           "CONCAT(p.Apellido, ' ', p.Nombre) AS Propietario " \
                           "FROM Reclamo r " \
                           "LEFT JOIN Usuario u ON r.id_usuario = u.id " \
                           "LEFT JOIN Propietario p ON u.id_propietario = p.id " \
                           "WHERE p.id = %s " \
                           "ORDER BY r.fecha DESC"
            
            cursor.execute(consulta_sql, (id_propietario, ))
            filas = cursor.fetchall()

            for fila in filas:
                reclamo = ReclamoModelo(
                    id=fila[0],
                    tipo=fila[1],
                    fecha=fila[2],
                    mensaje=fila[3],
                    foto=fila[4],
                    estado=fila[5],
                    id_usuario=fila[6],
                    nombrePropietario=fila[7]
                )
                reclamos.append(reclamo)

        except mysql.connector.Error as e:
            print("Error al obtener reclamos por propietario: ", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return reclamos

    def obtener_propietarios(self):

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "SELECT Id, CONCAT(Apellido, ' ', Nombre)" \
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

    def cambiar_estado(self, id_reclamo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            consulta_sql = "UPDATE Reclamo SET estado = 0 " \
                           "WHERE id = %s"
            cursor.execute(consulta_sql, (id_reclamo, ))
            conn.commit()
            return True, "Reclamo Revisado"
            
        except mysql.connector.Error as e:
            print("Error al cambiar estado:", e)
            return False, f"Error al Revisar el reclamo"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    