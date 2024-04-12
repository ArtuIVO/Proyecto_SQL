import random
import tkinter

import mysql.connector
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from cliente import Cliente
from list import Lista
from producto import Producto
from usuario import Usuarios
from venta import Factura

usuarios = Lista()
clientes = Lista()
ventas = Lista()
productos = Lista()
producto0 = Producto("Cursos Libres", 50, 500)
productos.append(producto0)

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
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Factura (
        num_factura INT AUTO_INCREMENT PRIMARY KEY,
        nombre LONGTEXT,
        tel INT,
        cantidad INT
    );
""")
conn.commit()


def mostrar_tablas():
    global conn, cursor
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

        cursor.execute("SELECT * FROM Factura")
        ventas_info = cursor.fetchall()

        etiqueta_clientes = tkinter.Label(ventana_tablas, text="Información de Facturas:")
        etiqueta_clientes.pack()

        for venta_info in ventas_info:
            etiqueta_cliente = tkinter.Label(ventana_tablas, text=venta_info)
            etiqueta_cliente.pack()

    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")


def generar_factura(nombre_cliente, nit, cantidad_producto, num_factura, productos):
    # Calcular el total
    precio_producto = 500  # Precio de producto (ejemplo)
    total = cantidad_producto * precio_producto

    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Heading1"]
    estilo_encabezado = estilos["Heading2"]
    estilo_normal = estilos["BodyText"]
    estilo_firma = ParagraphStyle(name="Firma", parent=estilo_normal, alignment=1)

    contenido = Lista()

    # Crear el lienzo para la factura
    doc = SimpleDocTemplate(f"Factura_{num_factura}.pdf", pagesize=letter)
    elementos = []

    # Logo de la empresa
    imagen_empresa = Image("30-AÑOS-AGREQUIMA.png", width=150, height=150)
    imagen_empresa.drawHeight = 1.5 * inch * imagen_empresa.drawHeight / imagen_empresa.drawWidth
    imagen_empresa.drawWidth = 1.5 * inch
    elementos.append(imagen_empresa)

    # Título de la factura
    elementos.append(Paragraph("FACTURA", estilo_titulo))

    # Detalles del cliente y factura
    detalles_cliente = [
        ["Cliente:", nombre_cliente],
        ["NIT:", nit],
        ["Número de Factura:", num_factura],
    ]
    tabla_detalles_cliente = Table(detalles_cliente)
    elementos.append(tabla_detalles_cliente)

    # Detalle del producto
    detalles_producto = [
        ["Cantidad:", cantidad_producto],
        ["Precio Unitario:", f"Q{precio_producto}"],
        ["Total:", f"Q{total}"],
    ]
    tabla_detalles_producto = Table(detalles_producto)
    elementos.append(tabla_detalles_producto)

    # Lista de productos y precios
    detalles_productos = [["Producto", "Precio"]]
    for producto, precio in productos.items():
        detalles_productos.append([producto, f"Q{precio}"])

    tabla_productos = Table(detalles_productos)
    tabla_productos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                         ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elementos.append(tabla_productos)

    # Espacios en blanco
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"<b>Total:</b> Q{total}", estilo_encabezado))
    elementos.append(Spacer(1, 50))
    elementos.append(Paragraph("Firma ________________________", estilo_firma))

    # Construir el PDF de la factura
    doc.build(elementos)


def update_new_facture():
    global conn, cursor

    def obtener_datos():
        nombre = cuadro_nombre.get()
        identificador = cuadro_contrasenia.get()
        celular = cuadro_celular.get()
        nombre1 = str(nombre)
        identificador1 = int(identificador)
        celular1 = int(celular)
        num_de_factura = int(random.randint(0, 999))
        productos = {}
        for x in range(celular1):
            productos[f"Producto{x + 1}"] = 500

        if ventas.search_by_ID_ventas(num_de_factura) is not None:
            etiqueta_error_id = tkinter.Label(ventana3, text="El No. de factura ya existe",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()
        else:
            generar_factura(nombre1, identificador1, celular1, num_de_factura, productos)
            new_facture = Factura(nombre1, identificador1, celular1, num_de_factura)
            ventas.append(new_facture)

            cursor = conn.cursor()
            cursor.execute("INSERT INTO Factura (nombre, tel, cantidad, num_factura) VALUES (%s, %s, %s, %s)",
                           (nombre, identificador, celular, num_de_factura))
            conn.commit()

            print(new_facture)
            etiqueta_aceptacion = tkinter.Label(ventana3, text="Datos aceptados correctamente",
                                                font=("times new roman", 12))
            etiqueta_aceptacion.pack()

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre del cliente, número de telefono y cantidad del "
                                             "producto comprado: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    etiqueta_nombre = tkinter.Label(ventana3, text="Nombre:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)
    etiqueta_contrasenia = tkinter.Label(ventana3, text="No. de nit:", font=("times new roman", 12))
    etiqueta_contrasenia.pack()
    cuadro_contrasenia = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_contrasenia.pack(pady=10)
    etiqueta_ID = tkinter.Label(ventana3, text="Cantidad del producto:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_celular = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_celular.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def delete_facture():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()
        identificador = int(identificador)
        if ventas.search_by_ID_ventas(identificador) is None:
            etiqueta_error_id = tkinter.Label(ventana3, text="El No. de factura ingresado no existe, vuelva a "
                                                             "intentarlo",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Factura encontrada:\n"
                                                                   f"{ventas.search_by_ID_ventas(identificador).data}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if ventas.search_by_ID_ventas(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El No. de factura ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    cursor.execute("DELETE FROM Factura WHERE num_factura = %s", (identificador,))
                    conn.commit()
                    ventas.deleate_by_ID_ventas(identificador)
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Factura eliminada",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            def boton_no():
                if ventas.search_by_ID_ventas(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El No. de factura ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    etiqueta_no_eliminado = tkinter.Label(ventana3, text="Factura no eliminada",
                                                          font=("times new roman", 12))
                    etiqueta_no_eliminado.pack()
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")

    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el Número de factura a eliminar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="No. Factura:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Aceptar", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def update_new_customer():
    global conn, cursor

    def obtener_datos():
        nombre = cuadro_nombre.get()
        identificador = cuadro_contrasenia.get()
        celular = cuadro_celular.get()

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

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre, ID y celular de su núevo cliente: ",
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
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def delete_customer():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()
        identificador = int(identificador)
        if clientes.search_by_ID_cleinte(identificador) is None:
            etiqueta_error_id = tkinter.Label(ventana3, text="El ID ingresado no existe, vuelva a intentarlo",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Cliente encontrado:\n"
                                                                   f"{clientes.search_by_ID_cleinte(identificador).data}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if clientes.search_by_ID_cleinte(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El ID ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    cursor.execute("DELETE FROM Clientes WHERE identificador = %s", (identificador,))
                    conn.commit()
                    clientes.delete_by_ID(identificador)
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Cliente eliminado",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            def boton_no():
                if clientes.search_by_ID_cleinte(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El ID ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Cliente no eliminado",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el ID del cliente a eliminar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="ID:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Aceptar", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def edit_customer():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()


    def obtener_datos():
        identificador = cuadro_ID.get()
        identificador = int(identificador)

        def actualizar_datos(identificador, nuevo_nombre, nuevo_telefono, nuevo_nit):
            nuevo_nombre = str(nuevo_nombre)
            nuevo_telefono = int(nuevo_telefono)
            nuevo_nit = int(nuevo_nit)

            if clientes.search_by_ID_cleinte(identificador) is None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El NIT ingresado no existe, vuelva a intentarlo",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()
            elif clientes.search_by_ID_cleinte(nuevo_nit) is not None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El NIT ingresado ya existe, vuelva a intentarlo",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()

            elif clientes.search_by_cel(nuevo_telefono) is not None:
                etiqueta_error_id = tkinter.Label(ventana3, text="El celular ya existe, vuelva a intentarlo",
                                                  font=("times new roman", 12))
                etiqueta_error_id.pack()

            else:
                cursor.execute("UPDATE Clientes SET nombre = %s, celular = %s, identificador = %s",
                               (nuevo_nombre, nuevo_telefono, nuevo_nit))
                conn.commit()
                clientes.search_by_ID_cleinte(identificador).data.nombre = nuevo_nombre
                clientes.search_by_ID_cleinte(identificador).data.celular = nuevo_telefono
                clientes.search_by_ID_cleinte(identificador).data.identificador = nuevo_nit
                etiqueta_editado = tkinter.Label(ventana3, text="Cliente editado", font=("times new roman", 12))
                etiqueta_editado.pack()
                limpiar_datos()

        if clientes.search_by_ID_cleinte(identificador) is None:
            etiqueta_error_id = tkinter.Label(ventana3, text="El NIT ingresado ya existe, vuelva a intentarlo",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Cliente encontrado:\n"
                                                                   f"{clientes.search_by_ID_cleinte(identificador).data}\n"
                                                                   f"Desea editar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                limpiar_datos()
                etiqueta_nuevo_nombre = tkinter.Label(ventana3, text="Ingrese el nuevo nombre: ",
                                                      font=("times new roman", 12))
                etiqueta_nuevo_nombre.pack()
                cuadro_nuevo_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nombre.pack(pady=10)
                etiqueta_nuevo_cel = tkinter.Label(ventana3, text="Ingrese el nuevo número de cel: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_cel.pack()
                cuadro_nuevo_cel = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_cel.pack(pady=10)
                etiqueta_nuevo_nit = tkinter.Label(ventana3, text="Ingrese el nuevo NIT: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_nit.pack()
                cuadro_nuevo_nit = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nit.pack(pady=10)

                boton_aceptar = tkinter.Button(ventana3, text="Aceptar", command=lambda: actualizar_datos(identificador,
                                                                                                          cuadro_nuevo_nombre.get(),
                                                                                                          cuadro_nuevo_cel.get(),
                                                                                                          cuadro_nuevo_nit.get()),
                                               bg="blue", fg="white", width=15, height=2, bd=12)
                boton_aceptar.pack(pady=10)

            def boton_no():
                if clientes.search_by_ID_cleinte(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El NIT ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Cliente no editado",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el NIT del cliente a editar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="NIT:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Aceptar", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)

    ventana3.mainloop()


def update_new_user():
    global conn, cursor

    def obtener_datos():
        nombre = cuadro_nombre.get()
        contrasenia = cuadro_contrasenia.get()
        identificador = cuadro_ID.get()
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
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def delete_user():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()
        identificador = int(identificador)
        if usuarios.search_by_ID_usuario(identificador) is None:
            etiqueta_error_id = tkinter.Label(ventana3, text="El ID ingresado no existe, vuelva a intentarlo",
                                              font=("times new roman", 12))
            etiqueta_error_id.pack()
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Usuario encontrado:\n"
                                                                   f"{usuarios.search_by_ID_usuario(identificador).data}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if usuarios.search_by_ID_usuario(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El ID ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    cursor.execute("DELETE FROM Usuarios WHERE identificador = %s", (identificador,))
                    conn.commit()
                    usuarios.delete_by_ID(identificador)
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Usuario eliminado",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            def boton_no():
                if usuarios.search_by_ID_usuario(identificador) is None:
                    etiqueta_error_id = tkinter.Label(ventana3,
                                                      text="El ID ingresado no existe, vuelva a intentarlo",
                                                      font=("times new roman", 12))
                    etiqueta_error_id.pack()
                else:
                    etiqueta_eliminado = tkinter.Label(ventana3, text="Usuario no eliminado",
                                                       font=("times new roman", 12))
                    etiqueta_eliminado.pack()
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el ID del usuario a eliminar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="ID:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Aceptar", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def mostrar_usuarios():
    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son los usuarios actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta4 = tkinter.Label(ventana3, text=f"{usuarios.transversal()}")
    etiqueta4.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def mostrar_facturas():
    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son las facturas actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta4 = tkinter.Label(ventana3, text=f"{ventas.transversal()}")
    etiqueta4.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def mostrar_clientes():
    ventana3 = tkinter.Tk()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son los clientes actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta4 = tkinter.Label(ventana3, text=f"{clientes.transversal()}")
    etiqueta4.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana3.mainloop()


def menu_de_usuarios():
    ventana4 = tkinter.Tk()
    ventana4.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana4, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana4, text="Agregar nuevos usuarios", command=update_new_user, bg="lime", fg="black",
                            width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana4, text="Eliminar usurios", command=delete_user, bg="green", fg="black", width=15,
                            height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana4, text="Mostrar todos los usuarios", command=mostrar_usuarios, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton4.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana4.mainloop()


def menu_de_clientes():
    ventana4 = tkinter.Tk()
    ventana4.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana4, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana4, text="Agregar nuevos clientes", command=update_new_customer, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana4, text="Eliminar clientes", command=delete_customer, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana4, text="Mostrar todos los clientes", command=mostrar_clientes, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton4.pack(pady=5)
    boton5 = tkinter.Button(ventana4, text="Editar un usuario", command=edit_customer, bg="green", fg="black", width=15,
                            height=2, bd=12)
    boton5.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana4.mainloop()


def menu_de_facturas():
    ventana4 = tkinter.Tk()
    ventana4.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana4, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana4, text="Hacer una factura", command=update_new_facture, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana4, text="Eliminar una factura", command=delete_facture, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana4, text="Mostrar todas las facturas", command=mostrar_facturas, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton4.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana4.mainloop()


def vermenu():
    ventana2 = tkinter.Tk()
    ventana2.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana2, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana2, text="Ver menú de usuarios", command=menu_de_usuarios, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana2, text="Ver menú de clientes", command=menu_de_clientes, bg="orange", fg="white",
                            width=15, height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana2, text="Ver menú de facturas", command=menu_de_facturas, bg="navy", fg="white",
                            width=15, height=2, bd=12)
    boton4.pack(pady=5)

    boton_mostrar_tablas = tkinter.Button(ventana2, text="Mostrar Tablas", command=mostrar_tablas, bg="purple",
                                          fg="white", width=15, height=2, bd=12)
    boton_mostrar_tablas.pack(pady=5)

    def regresar():
        ventana2.destroy()
        ventana.deiconify()

    boton_regresar = tkinter.Button(ventana2, text="Regresar al menú", command=regresar, bg="red", fg="white", width=15,
                                    height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana2.mainloop()


def salir():
    ventana.destroy()


etiqueta = tkinter.Label(ventana, text="BIENVENIDO AL PROGRAMA DE ADMINISTRACION DE USUARIOS Y CLIENTES",
                         font=("times new roman", 14))
etiqueta.pack(pady=20)
boton0 = tkinter.Button(ventana, text="Ver el menú", command=vermenu, font=("times new roman", 12), bg="blue",
                        fg="white", width=15, height=2, bd=12)
boton0.pack(pady=5)
boton1 = tkinter.Button(ventana, text="Salir", command=salir, font=("times new roman", 12), bg="red", fg="black",
                        width=15, height=2, bd=12)
boton1.pack(pady=5)

ventana.mainloop()
