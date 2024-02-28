import tkinter
import mysql.connector
from usuario import Usuarios
from list import Lista
from cliente import Cliente

usuarios = Lista()
clientes = Lista()

usuario0 = Usuarios("Arturo Alva", "Tusmuertos.com18", 1525)
usuarios.append(usuario0)
cliente0 = Cliente("Jose Daniel", 1525123, 33987855)
clientes.append(cliente0)

ventana = tkinter.Tk()
ventana.geometry("900x700")

conn = mysql.connector.connect(
    host="localhost",
    user="Arturo Alva",
    password="Tusmuertos.com18",
    database="Agronomia"
)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre LONGTEXT,
        contrasenia LONGTEXT,
        identificador INT
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre LONGTEXT,
        identificador INT,
        celular INT
    );
""")
cursor.close()
conn.close()


def mostrar_tablas():
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

        ventana_tablas = tkinter.Toplevel()
        ventana_tablas.title("Tablas de la base de datos")

        etiqueta_tablas = tkinter.Label(ventana_tablas, text="Tablas de la base de datos:")
        etiqueta_tablas.pack()

        for tabla in tablas:
            etiqueta_tabla = tkinter.Label(ventana_tablas, text=tabla[0])
            etiqueta_tabla.pack()

        # Mostrar la información de las listas en las tablas
        cursor.execute("SELECT * FROM Usuarios")
        usuarios_info = cursor.fetchall()

        etiqueta_usuarios = tkinter.Label(ventana_tablas, text="Información de Usuarios:")
        etiqueta_usuarios.pack()

        for usuario_info in usuarios_info:
            etiqueta_usuario = tkinter.Label(ventana_tablas, text=usuario_info)
            etiqueta_usuario.pack()

        cursor.execute("SELECT * FROM Clientes")
        clientes_info = cursor.fetchall()

        etiqueta_clientes = tkinter.Label(ventana_tablas, text="Información de Clientes:")
        etiqueta_clientes.pack()

        for cliente_info in clientes_info:
            etiqueta_cliente = tkinter.Label(ventana_tablas, text=cliente_info)
            etiqueta_cliente.pack()

    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")


def update_new_customer():
    def obtener_datos():
        nombre = cuadro_nombre.get()
        identificador = cuadro_contrasenia.get()
        celular = cuadro_celular.get()

        try:
            nombre1 = str(nombre)
            identificador1 = int(identificador)
            celular1 = int(celular)
            if clientes.search_by_ID_cleinte(identificador1) is not None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El ID ya existe",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()
            elif clientes.search_by_cel(celular1) is not None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El celular ya existe",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()
            else:
                new_customer = Cliente(nombre1, identificador1, celular1)
                clientes.append(new_customer)

                cursor = conn.cursor()
                cursor.execute("INSERT INTO Clientes (nombre, identificador, celular) VALUES (%s, %s, %s)",
                               (nombre, identificador, celular))
                conn.commit()

                print(new_customer)
                etiqueta_aceptacion = tkinter.Label(ventana3, text="Datos aceptados correctamente",
                                                    font=("times new roman", 12))
                etiqueta_aceptacion.pack()
        except ValueError:
            etiqueta_error_id = tkinter.Label(ventana3, text="ID o su número de telefono no son validos, por favor "
                                                             "ingresar solo números",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre, ID y celulcar de su núevo cliente: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    etiqueta_nombre = tkinter.Label(ventana3, text="Nombre:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)
    etiqueta_contrasenia = tkinter.Label(ventana3, text="Identificador:", font=("times new roman", 12))
    etiqueta_contrasenia.pack()
    cuadro_contrasenia = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_contrasenia.pack(pady=10)
    etiqueta_ID = tkinter.Label(ventana3, text="Celular:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_celular = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_celular.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def update_new_user():
    def obtener_datos():
        nombre = cuadro_nombre.get()
        contrasenia = cuadro_contrasenia.get()
        identificador = cuadro_ID.get()

        try:
            nombre = str(nombre)
            identificador = int(identificador)
            if usuarios.search_by_ID_usuario(identificador) is not None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El ID ya existe",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()
            else:
                new_user = Usuarios(nombre, contrasenia, identificador)
                usuarios.append(new_user)

                cursor = conn.cursor()
                cursor.execute("INSERT INTO Usuarios (nombre, contrasenia, identificador) VALUES (%s, %s, %s)",
                               (nombre, contrasenia, identificador))
                conn.commit()

                print(new_user)
                etiqueta_aceptacion = tkinter.Label(ventana3, text="Datos aceptados correctamente",
                                                    font=("times new roman", 12))
                etiqueta_aceptacion.pack()
        except ValueError:
            etiqueta_error_id = tkinter.Label(ventana3, text="ID no válida, por favor ingresar solo números",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre, contraseña e ID de su núevo usuario: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    etiqueta_nombre = tkinter.Label(ventana3, text="Nombre:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)
    etiqueta_contrasenia = tkinter.Label(ventana3, text="Contraseña:", font=("times new roman", 12))
    etiqueta_contrasenia.pack()
    cuadro_contrasenia = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_contrasenia.pack(pady=10)
    etiqueta_ID = tkinter.Label(ventana3, text="ID:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def vermenu():
    ventana2 = tkinter.Tk()
    ventana2.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana2, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana2, text="Agregar nuevo usuario", command=update_new_user)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana2, text="Agregar nuevo cliente", command=update_new_customer)
    boton3.pack(pady=5)

    boton_mostrar_tablas = tkinter.Button(ventana2, text="Mostrar Tablas", command=mostrar_tablas)
    boton_mostrar_tablas.pack(pady=5)

    def activacion():
        global conn
        server = "localhost"
        database = "Agronomia"
        primer_usuario = usuarios.head.data
        username = primer_usuario.nombre
        password = primer_usuario.contrasenia

        try:
            conn = mysql.connector.connect(
                host=server,
                database=database,
                user=username,
                password=password
            )

            if conn.is_connected():
                print('Conexión exitosa a la base de datos')

                cursor = conn.cursor()
                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre LONGTEXT,
                            contrasenia LONGTEXT,
                            identificador INT
                        );
                    """)
                conn.commit()

                cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Clientes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre LONGTEXT,
                            identificador INT,
                            celular INT
                        );
                    """)
                conn.commit()

        except mysql.connector.Error as e:
            print(f'Error al conectarse a la base de datos: {e}')

        finally:
            if conn is not None and conn.is_connected():
                etiqueta_activado = tkinter.Label(ventana2, text="Base de datos conectada correctamente",
                                                  font=("times new roman", 14))
                etiqueta_activado.pack(pady=20)

    boton4 = tkinter.Button(ventana2, text="Activar la base de datos", command=activacion)
    boton4.pack(pady=5)

    def regresar():
        ventana2.destroy()
        ventana.deiconify()

    boton_regresar = tkinter.Button(ventana2, text="Regresar al menú", command=regresar)
    boton_regresar.pack(pady=5)
    ventana2.mainloop()


def salir():
    ventana.destroy()


etiqueta = tkinter.Label(ventana, text="Menú", font=("times new roman", 14))
etiqueta.pack(pady=20)
boton0 = tkinter.Button(ventana, text="Ver el menú", command=vermenu)
boton0.pack(pady=5)
boton1 = tkinter.Button(ventana, text="Salir", command=salir)
boton1.pack(pady=5)

ventana.mainloop()
