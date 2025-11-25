import mysql.connector
from Modelo.propietario import PropietarioModelo
from Modelo.conexion import obtener_conexion

class PropietarioControlador:
    def __init__(self):
        pass

    def obtener_propietario_por_id(self, id_propietario):
            try:
                conn = obtener_conexion()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Propietario WHERE id = %s", (id_propietario,))
                propietario = cursor.fetchone()

                return propietario

            except Exception as e:
                print(f"Error al obtener el propietario: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    
    def obtener_todos(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT apellido, nombre, dni, telefono, estado, departamento, id FROM propietario")
            propietario = [PropietarioModelo(*fila) for fila in cursor.fetchall()]
            return propietario
        
        except Exception as e:
            print(f"Error al obtener los propietario: {e}")
            return []
        
        finally:
            if conn:
                conn.close()
            if cursor:
                 cursor.close()

    def nuevo_propietario(self, propietario: PropietarioModelo):
        try:
            if propietario.apellido != "" and propietario.nombre != "" and propietario.dni != "" and propietario.departamento != "":
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO propietario(apellido, nombre, dni, telefono, estado, departamento)" \
                               "VALUES(%s, %s, %s, %s, %s, %s)", 
                               (propietario.apellido, propietario.nombre, propietario.dni, propietario.telefono, propietario.estado, propietario.departamento))
                conn.commit()
                return True, "Propietario creado correctamente"
            else:
                return False, f"Faltan completar campos"

        except Exception as e:
            return False, f"Error al crear el propietario: {e}"
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close

    def editar_propietario(self, propietario : PropietarioModelo):
        try:
            if propietario.apellido != "" and propietario.nombre != "" and propietario.dni != "" and propietario.departamento != "":
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("UPDATE propietario SET apellido=%s, nombre= %s, dni= %s, telefono= %s, estado= %s, departamento= %s "
                               "WHERE id= %s",
                               (propietario.apellido, propietario.nombre, propietario.dni, propietario.telefono, propietario.estado, propietario.departamento, propietario.id))
                conn.commit()
                return True, "Propietario actualizado correctamente"
            else:
                return False, f"Apellido, Nombre y Correo son campos OBLIGATORIOS."
        except Exception as e:
            return False, f"Error al editar el propietario: ",e
        
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
    
    def eliminar_propietario(self, propietario_id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            # Obtener estado actual
            cursor.execute("SELECT estado FROM propietario WHERE id = %s", (propietario_id, ))
            fila = cursor.fetchone()
            if fila is None:
                raise ValueError("Propietario no encontrado")
            
            estado_actual = fila[0]
            nuevo_estado = not estado_actual   #Invertir el booleano
            #Actualizar el estado
            cursor.execute("UPDATE propietario SET estado= %s WHERE id=%s", (nuevo_estado, propietario_id))
            conn.commit()
            return True, "El propietario se eliminó correctamente."

        except mysql.connector.Error as e:
            return False, f"Error al desactivar el propietario: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
