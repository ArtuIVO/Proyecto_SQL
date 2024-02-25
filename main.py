import tkinter
from tkinter import Tk, Label, Button, Entry, StringVar
from usuario import Usuarios

import pyodbc

server = "LocalHost"
bd = "Usuarios"

usuario0 = Usuarios("Jorge Manuel", "Tusmuertos.com18", 1525)

ventana = tkinter.Tk()
ventana.geometry("900x700")


def vermenu():
    ventana2 = tkinter.Tk()
    ventana2.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana2, text="¿Que desea hacer?")
    etiqueta2.pack()
    boton2 = tkinter.Button(ventana2, text="Agregar nuevo usuario")
    boton2.pack()
    boton3 = tkinter.Button(ventana2, text="Agregar nuevo stock")
    boton3.pack()

    def regresar():
        ventana2.destroy()
        ventana.deiconify()

    boton_regresar = tkinter.Button(ventana2, text="Regresar al menú", command=regresar)
    boton_regresar.pack()
    ventana2.mainloop()


def salir():
    ventana.destroy()


etiqueta = tkinter.Label(ventana, text="Menú")
etiqueta.pack()
boton0 = tkinter.Button(ventana, text="Ver el menú", command=vermenu)
boton0.pack()
boton1 = tkinter.Button(ventana, text="Salir", command=salir)
boton1.pack()

ventana.mainloop()
