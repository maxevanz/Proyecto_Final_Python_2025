from .conexion import obtener_conexion

class EmpleadoModelo:

    def __init__(self, apellido, nombre, correo, telefono, estado, id=None):
        self.id = id
        self.apellido = apellido
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.estado = estado

    def obtener_empleado_por_id(id_empleado):
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

    @staticmethod
    def obtener_todos():
        conn = None
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

    def guardar(self):
        conn = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO empleado(apellido, nombre, correo, telefono, estado)" \
                           "VALUES(%s, %s, %s, %s, %s)", (self.apellido, self.nombre, self.correo, self.telefono, self.estado))
            conn.commit()
        except Exception as e:
            print(f"Error al guardar el empleado: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def editar(self):
        conn = None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("UPDATE empleado SET apellido=%s, nombre= %s, correo= %s, telefono= %s, estado= %s "
                           "WHERE id= %s",
                           (self.apellido, self.nombre, self.correo, self.telefono, self.estado, self.id))
            conn.commit()
        
        except Exception as e:
                print(f"Error al editar el empleado: {e}")
                raise
        
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar(id):
         conn = None
         try:
              conn = obtener_conexion()
              cursor = conn.cursor()

              # Obtener estado actual
              cursor.execute("SELECT estado FROM empleado WHERE id = %s", (id, ))
              fila = cursor.fetchone()

              if fila is None:
                   raise ValueError("Empleado no encontrado")
              
              estado_actual = fila[0]
              nuevo_estado = not estado_actual   #Invertir el booleano

              #Actualizar el estado
              cursor.execute("UPDATE empleado SET estado= %s WHERE id=%s", (nuevo_estado, id))
              conn.commit()

         except Exception as e:
              print(f"Error al editar el empleado: {e}")
              raise
        
         finally:
              if conn:
                   conn.close()
