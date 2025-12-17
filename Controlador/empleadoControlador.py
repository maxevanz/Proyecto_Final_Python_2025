import mysql.connector
from Modelo.empleado import EmpleadoModelo
from Modelo.conexion import obtener_conexion

class EmpleadoControlador:
    def __init__(self):
        pass

    def obtener_empleado_por_id(self, id_empleado):
            try:
                conn = obtener_conexion()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Empleado WHERE id = %s", (id_empleado,))
                empleado = cursor.fetchone()

                return empleado

            except Exception as e:
                print(f"Error al obtener el empleado: {e}")
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
            cursor.execute("SELECT apellido, nombre, correo, telefono, estado, id FROM empleado")
            empleados = [EmpleadoModelo(*fila) for fila in cursor.fetchall()]
            return empleados
        
        except Exception as e:
            print(f"Error al obtener los empleados: {e}")
            return []
        
        finally:
            if conn:
                conn.close()
            if cursor:
                 cursor.close()

    def nuevo_empleado(self, empleado: EmpleadoModelo):
        try:
            if empleado.apellido != "" and empleado.nombre != "" and empleado.correo != "":
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO empleado(apellido, nombre, correo, telefono, estado)" \
                               "VALUES(%s, %s, %s, %s, %s)", 
                               (empleado.apellido, empleado.nombre, empleado.correo, empleado.telefono, empleado.estado))
                conn.commit()
                return True, "Empleado creado correctamente"
            else:
                return False, f"Faltan completar campos"

        except mysql.connector.IntegrityError as e:
            return False, "⚠️ El correo ya existe en la base de datos"
        except Exception as e:
            return False, f"Error al crear el empleado: {e}"
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close

    def editar_empleado(self, empleado : EmpleadoModelo):
        try:
            if empleado.apellido != "" and empleado.nombre != "" and empleado.correo != "":
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("UPDATE empleado SET apellido=%s, nombre= %s, correo= %s, telefono= %s, estado= %s "
                               "WHERE id= %s",
                               (empleado.apellido, empleado.nombre, empleado.correo, empleado.telefono, empleado.estado, empleado.id))
                conn.commit()
                return True, "Empleado actualizado correctamente"
            else:
                return False, f"Apellido, Nombre y Correo son campos OBLIGATORIOS."
            
        except mysql.connector.IntegrityError as e:
            return False, "⚠️ El correo ya existe en la base de datos"
        except Exception as e:
            return False, f"Error al editar el empleado: ",e
        
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
    
    def eliminar_empleado(self, empleado_id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            # Obtener estado actual
            cursor.execute("SELECT estado FROM empleado WHERE id = %s", (empleado_id, ))
            fila = cursor.fetchone()
            if fila is None:
                raise ValueError("Empleado no encontrado")
            
            estado_actual = fila[0]
            nuevo_estado = not estado_actual   #Invertir el booleano
            #Actualizar el estado
            cursor.execute("UPDATE empleado SET estado= %s WHERE id=%s", (nuevo_estado, empleado_id))
            conn.commit()
            return True, "El empleado se eliminó correctamente."

        except mysql.connector.Error as e:
            return False, f"Error al desactivar el empleado: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
