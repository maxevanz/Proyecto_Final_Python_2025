Detalle Proyecto Final - Trayecto Formacion Profesional PROGRAMACION 2025

Antes de ejecutar el Sistema debemos instalar un par de librerias, modificar el archivo inicializador_datos.py y conexion.py, paso a detallar:


1° - Instalar librerias necesarias:
*   pip install mysql-connector-python
*   pip install bcrypt
*   pip install Pillow
*   pip install tkcalendar
*   pip install fpdf2

2° - Modificar el archivo inicializador_datos.py, en la clase:
    def crear_esquema_y_tablas():
        try:
            # Paso 1: crear la base si no existe
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="M@nudiaz1",           <-- Modificar el password y user de ser necesario 
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
                password="M@nudiaz1",           <-- Modificar el password y user de ser necesario 
                database="porteria",
                port="3306"
            )

3° - Modificar el archivo conexion.py, que se encuentra en la carpeta Modelo:
    def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "M@nudiaz1",             <-- Modificar el password y user de ser necesario 
        database = "porteria"
        )
        
        print("Éxito")
        return conexion
    except mysql.connector.Error as error:
        print("Error al conectar con la base de datos {}".format(error))


4° - Una vez instaladas las librerias y modificados los 2 archivos, procedemos a ejecutar el archivo inicializador_datos.py de la siguient manera:

    * nos posicionamos en el archivo raiz(main.py) y presionamos Ctrl+Ñ, esto para abrir la consola
    * entonces escribimos: python Utilidades/inicializador_datos.py
    *Nos deberia largar un mensaje por consola que la base, las tablas y los registros se generaron y cargaron correctamente

    