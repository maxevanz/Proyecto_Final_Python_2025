import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from datetime import datetime
from Modelo.conexion import obtener_conexion  # ajustá si tu función está en otro módulo
import mysql.connector

def crear_esquema_y_tablas():
    try:
        # Paso 1: crear la base si no existe
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="M@nudiaz1",
            port="3306"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS porteria DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;")
        conn.commit()
        cursor.close()
        conn.close()

        # Paso 2: conectar ya a la base y crear tablas
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="M@nudiaz1",
            database="porteria",
            port="3306"
        )
        cursor = conn.cursor()

        # Crear tablas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
          id INT NOT NULL AUTO_INCREMENT,
          Apellido VARCHAR(50) NOT NULL,
          Nombre VARCHAR(50) NOT NULL,
          Correo VARCHAR(150) NOT NULL,
          Telefono VARCHAR(15) NOT NULL,
          Estado TINYINT(1) NOT NULL DEFAULT '1',
          PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS propietario (
          Id INT NOT NULL AUTO_INCREMENT,
          Apellido VARCHAR(50) NOT NULL,
          Nombre VARCHAR(50) NOT NULL,
          DNI VARCHAR(15) NOT NULL,
          Telefono VARCHAR(15) NOT NULL,
          Estado TINYINT(1) NOT NULL DEFAULT '1',
          Departamento VARCHAR(20) NOT NULL,
          PRIMARY KEY (Id),
          INDEX (DNI ASC)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
          id INT NOT NULL AUTO_INCREMENT,
          NombreUsuario VARCHAR(50) NOT NULL,
          Contraseña VARCHAR(255) NOT NULL,
          Rol ENUM('admin','supervisor','usuario','propietario') NOT NULL,
          Estado TINYINT(1) NOT NULL,
          id_empleado INT NULL,
          id_propietario INT NULL,
          PRIMARY KEY (id),
          UNIQUE INDEX (NombreUsuario ASC),
          FOREIGN KEY (id_empleado) REFERENCES empleado(id),
          FOREIGN KEY (id_propietario) REFERENCES propietario(Id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
          id INT NOT NULL AUTO_INCREMENT,
          tipo ENUM('ingreso','egreso','paqueteria','visitas','otros') NOT NULL,
          fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          observaciones VARCHAR(500),
          imagen VARCHAR(255),
          id_usuario INT NOT NULL,
          id_propietario INT NULL,
          PRIMARY KEY (id),
          FOREIGN KEY (id_usuario) REFERENCES usuario(id),
          FOREIGN KEY (id_propietario) REFERENCES propietario(Id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS novedades (
          id INT NOT NULL AUTO_INCREMENT,
          Tipo ENUM('empleado','propietario','todos') NOT NULL,
          Fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          Titulo VARCHAR(50),
          Descripcion VARCHAR(500) NOT NULL,
          Estado TINYINT(1) NOT NULL DEFAULT '1',
          PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reclamo (
          Id INT NOT NULL AUTO_INCREMENT,
          Tipo ENUM('portero','vecinos','edificio','otros') NOT NULL,
          Fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
          Mensaje VARCHAR(500) NOT NULL,
          Foto VARCHAR(255),
          Estado TINYINT(1) NOT NULL DEFAULT '1',
          id_usuario INT NOT NULL,
          PRIMARY KEY (Id),
          FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)

        conn.commit()
        print("✅ Esquema y tablas creados/verificados correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al crear esquema/tablas:", e)
    finally:
        cursor.close()
        conn.close()

def insertar_empleados(cursor):
    empleados = [
        ("Admin", "Admin", "admin@gmail.com", "", 1),
        ("López", "Ana", "lopez@gmail.com", "3816973021", 1),
        ("Grillo", "Pedro", "grillo@gmail.com", "3863621934", 1)
    ]
    for apellido, nombre, correo, telefono, estado in empleados:
        cursor.execute("INSERT INTO Empleado (Apellido, Nombre, Correo, Telefono, Estado) " \
                       "VALUES (%s, %s, %s, %s, %s)"
                       , (apellido, nombre, correo, telefono, estado))

def insertar_propietarios(cursor):
    propietarios = [
        ("Gómez", "Laura", "30555030", "3813021014", 1, "1ro B"),
        ("Pérez", "Juan", "32979001", "3814637100", 1, "2do F"),
        ("Rodríguez", "Ana", "29073409", "3863679312", 1, "PB H"),
        ("Peralta", "Hernesto", "31409713", "3812903770", 1, "3ra A")
    ]
    for apellido, nombre, dni, telefono, estado, dpto in propietarios:
        cursor.execute("INSERT INTO Propietario (Apellido, Nombre, DNI, Telefono, Estado, Departamento) " \
                       "VALUES (%s, %s, %s, %s, %s, %s)"
                       , (apellido, nombre, dni, telefono, estado, dpto))

def insertar_usuarios(cursor):
    usuarios = [
        ("1234", "$2a$12$lDg.OD1xqqAmS9TdgNoAI.wvi7kA03IAct856H79z8TP2ONyQuoGq", "admin", 1, 1, None),  # id_propietario 1
        ("lopez", "$$2a$12$lDg.OD1xqqAmS9TdgNoAI.wvi7kA03IAct856H79z8TP2ONyQuoGq", "usuario", 1, 2, None),
        ("lgomez", "$2a$12$lDg.OD1xqqAmS9TdgNoAI.wvi7kA03IAct856H79z8TP2ONyQuoGq", "propietario",1, None, 1),
    ]
    for usuario, clave, rol, estado, id_empleado, id_prop in usuarios:
        cursor.execute("INSERT INTO Usuario (NombreUsuario, Contraseña, Rol, Estado, id_empleado, id_propietario) " \
                       "VALUES (%s, %s, %s, %s, %s, %s)", (usuario, clave, rol, estado, id_empleado, id_prop))

def insertar_eventos(cursor):
    eventos = [
        ("ingreso", datetime(2025, 12, 2), "Ingreso acompañado con una mujer y un niño", None, 2, None),
        ("egreso", datetime(2025, 12, 3), "Se retiran los acompaña", None, 2, 1),
    ]
    for tipo, fecha, observ, imagen, id_usuario, id_propietario in eventos:
        cursor.execute("INSERT INTO eventos (Tipo, Fecha, Observaciones, imagen, id_usuario, id_propietario) " \
                       "VALUES (%s, %s, %s, %s, %s, %s)"
                       , (tipo, fecha, observ, imagen, id_usuario, id_propietario))


def inicializar_datos():
    crear_esquema_y_tablas()   # primero creo base y tablas
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        insertar_empleados(cursor)
        insertar_propietarios(cursor)
        insertar_usuarios(cursor)        
        insertar_eventos(cursor)

        conn.commit()
        print("✅ Datos iniciales cargados correctamente.")
    except Exception as e:
        print("❌ Error al inicializar datos:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    inicializar_datos()
