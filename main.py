import tkinter
from usuario import Usuarios
from list import Lista
import mysql.connector
from cliente import Cliente

usuarios = Lista()
usuario0 = Usuarios("Arturo Alva", "Tusmuertos.com18", 1525)
usuarios.append(usuario0)

ventana = tkinter.Tk()
ventana.geometry("900x700")

conn = None


def vermenu():
    ventana2 = tkinter.Tk()
    ventana2.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana2, text="¿Que desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana2, text="Agregar nuevo usuario")
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana2, text="Agregar nuevo stock")
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana2, text="Agregar nuevo cliente")
    boton4.pack(pady=5)

    def activacion():
        global conn
        server = "localhost"
        database = "Agronomia"
        primer_usuario = usuarios[0]
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


        except mysql.connector.Error as e:
            print(f'Error al conectarse a la base de datos: {e}')

        finally:
            if conn is not None and conn.is_connected():
                conn.close()
                print('Conexión cerrada')

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


etiqueta = tkinter.Label(ventana, text="Menú",font=("times new roman", 14))
etiqueta.pack(pady=20)
boton0 = tkinter.Button(ventana, text="Ver el menú", command=vermenu)
boton0.pack(pady=5)
boton1 = tkinter.Button(ventana, text="Salir", command=salir)
boton1.pack(pady=5)

ventana.mainloop()
