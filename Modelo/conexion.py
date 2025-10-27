import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "M@nudiaz1",
        database = "Porteria"
        )
        
        print("Éxito")
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar con la base de datos {}".format(error))
        