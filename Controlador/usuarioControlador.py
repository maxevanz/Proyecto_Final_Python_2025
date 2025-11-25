#pip install bcrypt         -> alagoritmo de Hash para encriptar contraseñas

import mysql.connector
from Modelo.conexion import obtener_conexion
from Modelo.usuario import UsuarioModelo
import bcrypt

class UsuarioControlador:

    def __init__(self):
        pass

    def verificar_usuario(nombreusuario, contraseña):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            consulta_sql = "SELECT * FROM Usuario WHERE NombreUsuario = %s AND Estado = TRUE"
            cursor.execute(consulta_sql, (nombreusuario,))
            resultado = cursor.fetchone()                

            if resultado:
                has_guardado = resultado["Contraseña"]
                #Asegurar que el hash esté en bytes
                if isinstance(has_guardado, str):
                    has_guardado = has_guardado.encode('utf-8')

                #Validar formato del hash
                if has_guardado.startswith(b"$2b$") or has_guardado.startswith(b"$2a$"): 
                    if bcrypt.checkpw(contraseña.encode('utf-8'), has_guardado):
                        return resultado
                else:
                    print("Error: la contraseña almacenada no es un hash valido")
            return None     #credenciales incorrectas
        
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def obtener_usuarios(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            consulta_sql = "SELECT u.id, " \
                           "u.NombreUsuario, " \
                           "u.Contraseña, " \
                           "u.Rol, " \
                           "u.Estado, " \
                           "COALESCE(CONCAT(e.Apellido, ', ', e.Nombre), " \
                           "CONCAT(p.Apellido, ', ', p.Nombre)) AS NombreAsociado " \
                           "FROM " \
                           "Usuario u " \
                           "LEFT JOIN Empleado e ON u.id_empleado = e.id " \
                           "LEFT JOIN Propietario p ON u.id_propietario = p.id "
            cursor.execute(consulta_sql)
            usuarios = cursor.fetchall()
            return usuarios
        
        except mysql.connector.Error as e:
            print("Error al obtener usuarios: ", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def crear_usuario(self, usuario : UsuarioModelo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            # Encriptar la contraseña
            hashed = bcrypt.hashpw(usuario.contraseña.encode('utf-8'), bcrypt.gensalt())

            consulta_sql = "INSERT INTO Usuario(NombreUsuario, Contraseña, Rol, Estado)" \
                           "VALUES(%s, %s, %s, %s)"
            valores = (usuario.nombreusuario, hashed, usuario.rol, usuario.estado)
            cursor.execute(consulta_sql, valores)
            conn.commit()
            id_creado = cursor.lastrowid

            return id_creado    #devuelve el id del nuevo usuario

        except mysql.connector.Error as e:
            print(f"Error al crear el usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
    def vincular_empleado(self, id_empleado, id_usuario):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            consulta_sql = "UPDATE Usuario SET id_empleado =%s WHERE id = %s"
            valores = (id_empleado, id_usuario)
            cursor.execute(consulta_sql, valores)
            conn.commit()

            return True, "Usuario creado y vinculado"
        
        except mysql.connector.IntegrityError as e:
            return False, "El nombre de usuario o empleado ya está asignado a otro usuario."
        except mysql.connector.Error as e:
            return False, f"Error al vincular usuario con empleado: ",e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def vincular_propietario(self, id_propietario, id_usuario):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            consulta_sql = "UPDATE Usuario SET id_propietario =%s WHERE id = %s"
            valores = (id_propietario, id_usuario)
            cursor.execute(consulta_sql, valores)
            conn.commit()

            return True, "Usuario creado y vinculado"
        
        except mysql.connector.IntegrityError as e:
            return False, "El nombre de usuario o propietario ya está asignado a otro usuario."
        except mysql.connector.Error as e:
            return False, f"Error al vincular usuario con propietario: ",e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def editar_usuario(self, usuario : UsuarioModelo):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Detectar si la contraseña ya está encriptada (por ejemplo, empieza con $2b$)
            if usuario.contraseña.startswith("$2b$"):
                hashed = usuario.contraseña  # ya encriptada
            else:
                # Encriptar la contraseña
                hashed = bcrypt.hashpw(usuario.contraseña.encode('utf-8'), bcrypt.gensalt())

            consulta_sql = "UPDATE Usuario SET " \
                           "Contraseña = %s, Rol = %s WHERE id = %s"
            valores = (hashed, usuario.rol, usuario.id)
            
            cursor.execute(consulta_sql, valores)
            conn.commit()
            return True, "Usuario actualizado correctamente"
        except mysql.connector.IntegrityError as e:
            return False, "El nombre de usuario o empleado ya está asignado a otro usuario."
        except mysql.connector.Error as e:
            return False, f"Error al editar el usuario: ",e
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
        
    def activar_desactivar_usuario(self, usuario_id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Obtener estado actual
            cursor.execute("SELECT Estado FROM Usuario WHERE id = %s", (usuario_id, ))
            fila = cursor.fetchone()
            if fila is None:
                raise ValueError("Usuario no encontrado")
            
            estado_actual = fila[0]
            nuevo_estado = not estado_actual   #Invertir el booleano

            #Actualizar el estado
            cursor.execute("UPDATE Usuario SET Estado= %s WHERE id=%s", (nuevo_estado, usuario_id))
            conn.commit()

            return True, "El usuario se Activó/Desactivó correctamente."

        except mysql.connector.Error as e:
            return False, f"Error al desactivar el usuario: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_empleados_disponibles(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            consulta_sql = "SELECT e.id, e.apellido, e.nombre " \
                           "FROM Empleado e " \
                           "LEFT JOIN Usuario u ON e.id = u.id_empleado " \
                           "WHERE u.id_empleado IS NULL AND e.estado = 1"
            
            cursor.execute(consulta_sql)
            empleados = cursor.fetchall()
            return empleados
        
        except mysql.connector.Error as e:
            print("Error al obtener empleados disponibles: ",e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_propietarios_disponibles(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            consulta_sql = "SELECT p.id, p.apellido, p.nombre " \
                           "FROM Prpietario p " \
                           "LEFT JOIN Usuario u ON e.id = p.id_propietario " \
                           "WHERE u.id_propietario IS NULL AND e.estado = 1"
            
            cursor.execute(consulta_sql)
            propietarios = cursor.fetchall()
            return propietarios
        
        except mysql.connector.Error as e:
            print("Error al obtener propietarios disponibles: ",e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    #####FUNCIONES PARA FILTRAR USUARIOS POR ROL########
    def obtener_empleados(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            consulta_sql = "SELECT e.id, CONCAT(e.Apellido, ' ', e.Nombre) " \
                           "FROM Empleado e " \
                           "LEFT JOIN Usuario u ON e.id = u.id_empleado " \
                           "WHERE u.id_empleado IS NULL AND e.estado = 1"
            cursor.execute(consulta_sql)
            empleados = cursor.fetchall()
            return empleados
        
        except mysql.connector.Error as e:
            print("Error al obtener empleados: ", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_propietarios(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            consulta_sql = "SELECT p.id, CONCAT(p.Apellido, ' ', p.Nombre) " \
                           "FROM Propietario p " \
                           "LEFT JOIN Usuario u ON p.id = u.id_propietario " \
                           "WHERE u.id_propietario IS NULL AND p.estado = 1"
            cursor.execute(consulta_sql)
            propietarios = cursor.fetchall()
            return propietarios
        
        except mysql.connector.Error as e:
            print("Error al obtener propietarios: ", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_entidades_por_rol(self, rol):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            if rol == "propietario":
                return self.obtener_propietarios()
            else:
                return self.obtener_empleados()
        
        except mysql.connector.Error as e:
            print("Error al obtener propietarios: ", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()