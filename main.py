import random
import tkinter
from tkinter import messagebox, simpledialog

import mysql.connector
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from list import Lista

productos_seleccionados = []

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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        num_producto INT AUTO_INCREMENT PRIMARY KEY,
        nombre LONGTEXT,
        stock INT,
        precio FLOAT
    );
""")
conn.commit()


def mostrar_tablas():
    global conn, cursor
    ventana_tablas = tkinter.Toplevel()
    ventana_tablas.title("Tablas de la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

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

        cursor.execute("SELECT * FROM Productos")
        productos_info = cursor.fetchall()

        etiqueta_prodcuto = tkinter.Label(ventana_tablas, text="Información de Producto:")
        etiqueta_prodcuto.pack()

        for productos_info in productos_info:
            etiqueta_prodcuto = tkinter.Label(ventana_tablas, text=productos_info)
            etiqueta_prodcuto.pack()

    except mysql.connector.Error as e:
        print(f"Error al obtener las tablas: {e}")

    def regresar():
        ventana_tablas.destroy()

    boton_regresar = tkinter.Button(ventana_tablas, text="Regresar al menú", command=regresar, bg="red", fg="white",
                                    width=13,
                                    height=2, bd=12)
    boton_regresar.pack(pady=5)


def generar_factura(nombre_cliente, nit_cliente, productos_seleccionados):
    try:
        num_factura = random.randint(0, 100000)
        doc = SimpleDocTemplate(f"Factura_{num_factura}.pdf", pagesize=letter)

        # Crear un StyleSheet
        styles = getSampleStyleSheet()

        elementos = []

        # Agregar el logo al inicio de la factura
        logo_path = "30-AÑOS-AGREQUIMA.png"  # Ruta de la imagen del logo
        logo = Image(logo_path, width=200, height=100)  # Ajustar el tamaño de la imagen según sea necesario
        elementos.append(logo)

        contenido = [
            f"Cliente: {nombre_cliente}",
            f"NIT: {nit_cliente}",
            f"Número de Factura: {num_factura}"
        ]

        # Usar el estilo 'Normal' del StyleSheet para los Paragraph
        elementos.extend([Paragraph(line, styles['Normal']) for line in contenido])

        detalles_productos = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]
        total_factura = 0

        for num_producto, cantidad in productos_seleccionados:
            cursor.execute("SELECT nombre, precio FROM Productos WHERE num_producto = %s", (num_producto,))
            producto = cursor.fetchone()

            if producto:
                nombre_producto = producto[0]
                precio_producto = producto[1]
                subtotal_producto = cantidad * precio_producto
                detalles_productos.append(
                    [nombre_producto, str(cantidad), f"Q{precio_producto:.2f}", f"Q{subtotal_producto:.2f}"])
                total_factura += subtotal_producto

        tabla_productos = Table(detalles_productos)
        # Definir el estilo de la tabla correctamente
        estilo_tabla = TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Borde interno
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # Borde externo
        ])
        tabla_productos.setStyle(estilo_tabla)
        elementos.append(tabla_productos)

        elementos.append(Paragraph(f"Total: Q{total_factura:.2f}", styles['Heading1']))  # Ejemplo de otro estilo

        doc.build(elementos)

        messagebox.showinfo("¡ÉXITO!", f"Factura generada exitosamente: Factura_{num_factura}.pdf")

        # Guardar factura en la base de datos
        cursor.execute("INSERT INTO Factura (num_factura, nombre, tel, cantidad) VALUES (%s, %s, %s, %s)",
                       (num_factura, nombre_cliente, nit_cliente, len(productos_seleccionados)))
        conn.commit()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al generar la factura: {e}")


def update_new_facture():
    global conn, cursor

    def obtener_datos():
        global conn, cursor
        nombre = cuadro_nombre.get()
        identificador = cuadro_contrasenia.get()
        celular = cuadro_celular.get()

        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return
        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return
        if not celular:
            messagebox.showerror("Error", "Por favor, ingresa un número de teléfono válido (número entero).")
            return

        nombre = str(nombre)
        try:
            identificador = int(identificador)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return

        try:
            celular = int(celular)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número de teléfono válido (número entero).")
            return

        num_de_factura = random.randint(0, 999)
        productos = {}
        for x in range(celular):
            productos[f"Producto{x + 1}"] = 500

        consulta = "SELECT * FROM Factura WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un número de factura válido.")
            return
        else:
            cursor.execute("INSERT INTO Factura (nombre, tel, cantidad, num_factura) VALUES (%s, %s, %s, %s)",
                           (nombre, identificador, celular, num_de_factura))
            conn.commit()
            messagebox.showinfo("¡ÉXITO!", "Se creó la factura correctamente.")

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")

    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre del cliente, NIT y cantidad del producto comprado:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_nombre = tkinter.Label(ventana3, text="Nombre:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)

    etiqueta_contrasenia = tkinter.Label(ventana3, text="NIT:", font=("times new roman", 12))
    etiqueta_contrasenia.pack()
    cuadro_contrasenia = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_contrasenia.pack(pady=10)

    etiqueta_celular = tkinter.Label(ventana3, text="Cantidad del producto:", font=("times new roman", 12))
    etiqueta_celular.pack()
    cuadro_celular = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_celular.pack(pady=10)

    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=lambda: obtener_datos(conn, cursor),
                                         bg="blue", fg="white", width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al Menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def delete_facture():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()

        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido (número entero).")
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido (número entero).")
        consulta = "SELECT * FROM Factura WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un número de factura válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Factura encontrada:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea eliminar la factura ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingrese un número de factura válido")
                else:
                    cursor.execute("DELETE FROM Factura WHERE num_factura = %s", (identificador,))
                    conn.commit()
                    messagebox.showinfo("¡EXITO!", "Factura eliminado correctamente")
                    limpiar_datos()

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un número de factura válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su factura no fue eliminada")

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
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


def update_new_customer():
    global conn, cursor

    def obtener_datos():
        global conn, cursor
        nombre = cuadro_nombre.get()
        identificador = cuadro_contrasenia.get()
        celular = cuadro_celular.get()

        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return
        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return
        if not celular:
            messagebox.showerror("Error", "Por favor, ingresa un No. de celular válido (número entero).")
        try:
            nombre1 = str(nombre)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
        try:
            identificador1 = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido (número entero).")

        try:
            celular1 = int(celular)

        except:
            messagebox.showerror("Error", "Por favor, ingresa un No. de celular válido (número entero).")
            return

        consulta = "SELECT * FROM Clientes WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Clientes (nombre, identificador, celular) VALUES (%s, %s, %s)",
                           (nombre1, identificador1, celular1))
            conn.commit()
            messagebox.showinfo("¡EXITO!", "Se agrego su cliente correctamente")

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el nombre, NIT y celular de su núevo cliente: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    etiqueta_nombre = tkinter.Label(ventana3, text="Nombre:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)
    etiqueta_contrasenia = tkinter.Label(ventana3, text="NIT:", font=("times new roman", 12))
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


def delete_customer():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")
        consulta = "SELECT * FROM Clientes WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Cliente encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")
                else:
                    cursor.execute("DELETE FROM Clientes WHERE identificador = %s", (identificador,))
                    conn.commit()
                    messagebox.showinfo("¡EXITO!", "Su cliente fue eliminado correctamente")
                    limpiar_datos()

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su cliente no fue eliminado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el NIT del cliente a eliminar: ",
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


def edit_customer():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def limpiar_datos_actualizados():
        etiqueta_nuevo_nombre.pack_forget()
        cuadro_nuevo_nombre.pack_forget()
        etiqueta_nuevo_cel.pack_forget()
        cuadro_nuevo_cel.pack_forget()
        etiqueta_nuevo_nit.pack_forget()
        cuadro_nuevo_nit.pack_forget()
        boton_aceptar.pack_forget()

    def actualizar_datos(identificador, nuevo_nombre, nuevo_telefono, nuevo_nit):
        if not nuevo_nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return

        if not nuevo_telefono:
            messagebox.showerror("Error", "Por favor, ingresa un número de teléfono válido.")
            return

        if not nuevo_nit:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")

        try:
            nuevo_telefono = int(nuevo_telefono)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un número de teléfono válido (número entero).")
            return

        try:
            nuevo_nit = int(nuevo_nit)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return

        consulta = "SELECT * FROM Clientes WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")
        else:
            cursor.execute("UPDATE Clientes SET nombre = %s, celular = %s, identificador = %s",
                           (nuevo_nombre, nuevo_telefono, nuevo_nit))
            conn.commit()
            messagebox.showinfo("¡EXITO!", "Se agrego a su cliente correctamente")
            limpiar_datos_actualizados()

    def obtener_datos():
        identificador = cuadro_ID.get()

        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un NIT válido (número entero).")
            return

        consulta = "SELECT * FROM Clientes WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Cliente encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea editar al cliente ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                limpiar_datos()
                global etiqueta_nuevo_nombre, cuadro_nuevo_nombre, etiqueta_nuevo_cel, cuadro_nuevo_cel, etiqueta_nuevo_nit, cuadro_nuevo_nit, boton_aceptar
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

                boton_aceptar = tkinter.Button(ventana3, text="Aceptar",
                                               command=lambda: actualizar_datos(identificador,
                                                                                cuadro_nuevo_nombre.get(),
                                                                                cuadro_nuevo_cel.get(),
                                                                                cuadro_nuevo_nit.get()),
                                               bg="blue", fg="white", width=15, height=2, bd=12)
                boton_aceptar.pack(pady=10)

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un NIT válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su cliente no fue editado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
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


def update_new_user():
    global conn, cursor

    def obtener_datos():
        global conn, cursor
        nombre = cuadro_nombre.get()
        contrasenia = cuadro_contrasenia.get()
        identificador = cuadro_ID.get()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return
        if not contrasenia:
            messagebox.showerror("Error", "Por favor, ingresa un contraseña válido.")
            return
        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        try:
            nombre = str(nombre)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")

        consulta = "SELECT * FROM Usuarios WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Usuarios (nombre, contrasenia, identificador) VALUES (%s, %s, %s)",
                           (nombre, contrasenia, identificador))

            conn.commit()
            messagebox.showinfo("¡EXITO!", "Se agrego a su usuarios correctamente")

    ventana3 = tkinter.Toplevel()
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


def delete_user():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        identificador = cuadro_ID.get()
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        consulta = "SELECT * FROM Usuarios WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Usuario encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
                else:
                    cursor.execute("DELETE FROM Usuarios WHERE identificador = %s", (identificador,))
                    conn.commit()
                    messagebox.showinfo("¡EXITO!", "Su usuarios a sido eliminado correctamete")
                    limpiar_datos()

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su usuarios no fue eliminado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
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


def edit_user():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def limpiar_datos_actualizados():
        etiqueta_nuevo_nombre.pack_forget()
        cuadro_nuevo_nombre.pack_forget()
        etiqueta_nuevo_cel.pack_forget()
        cuadro_nuevo_cel.pack_forget()
        etiqueta_nuevo_nit.pack_forget()
        cuadro_nuevo_nit.pack_forget()
        boton_aceptar.pack_forget()

    def actualizar_datos(identificador, nuevo_nombre, nuevo_telefono, nuevo_nit):
        nuevo_nombre = str(nuevo_nombre)
        nuevo_telefono = str(nuevo_telefono)
        nuevo_nit = int(nuevo_nit)

        if not nuevo_nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return

        if not nuevo_telefono:
            messagebox.showerror("Error", "Por favor, ingresa una contraseña válido.")
            return

        try:
            nuevo_nit = int(nuevo_nit)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido (número entero).")
            return

        consulta = "SELECT * FROM Usuarios WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            cursor.execute("UPDATE Usuarios SET nombre = %s, contrasenia = %s, identificador = %s",
                           (nuevo_nombre, nuevo_telefono, nuevo_nit))
            conn.commit()
            messagebox.showinfo("¡EXITO!", "Su usuario fue editado correctamente")
            limpiar_datos_actualizados()

    def obtener_datos():
        identificador = cuadro_ID.get().strip()

        if not identificador:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
            return

        try:
            identificador = int(identificador)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido (número entero).")
            return
        consulta = "SELECT * FROM Usuarios WHERE identificador = %s"
        cursor.execute(consulta, (identificador,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Usuario encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea editar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                limpiar_datos()
                global etiqueta_nuevo_nombre, cuadro_nuevo_nombre, etiqueta_nuevo_cel, cuadro_nuevo_cel, etiqueta_nuevo_nit, cuadro_nuevo_nit, boton_aceptar
                etiqueta_nuevo_nombre = tkinter.Label(ventana3, text="Ingrese el nuevo nombre: ",
                                                      font=("times new roman", 12))
                etiqueta_nuevo_nombre.pack()
                cuadro_nuevo_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nombre.pack(pady=10)
                etiqueta_nuevo_cel = tkinter.Label(ventana3, text="Ingrese la nueva contraseña: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_cel.pack()
                cuadro_nuevo_cel = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_cel.pack(pady=10)
                etiqueta_nuevo_nit = tkinter.Label(ventana3, text="Ingrese el nuevo ID: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_nit.pack()
                cuadro_nuevo_nit = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nit.pack(pady=10)

                boton_aceptar = tkinter.Button(ventana3, text="Aceptar",
                                               command=lambda: actualizar_datos(identificador,
                                                                                cuadro_nuevo_nombre.get(),
                                                                                cuadro_nuevo_cel.get(),
                                                                                cuadro_nuevo_nit.get()),
                                               bg="blue", fg="white", width=15, height=2, bd=12)
                boton_aceptar.pack(pady=10)

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su usuarios no fue editado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el ID del usuario a editar: ",
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


def mostrar_usuarios():
    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son los usuarios actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios_info = cursor.fetchall()

    etiqueta_usuarios = tkinter.Label(ventana3, text="Información de Usuarios:")
    etiqueta_usuarios.pack()

    for usuario_info in usuarios_info:
        etiqueta_usuario = tkinter.Label(ventana3, text=usuario_info)
        etiqueta_usuario.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def mostrar_facturas():
    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son las facturas actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    cursor.execute("SELECT * FROM Factura")
    ventas_info = cursor.fetchall()

    etiqueta_clientes = tkinter.Label(ventana3, text="Información de Facturas:")
    etiqueta_clientes.pack()

    for venta_info in ventas_info:
        etiqueta_cliente = tkinter.Label(ventana3, text=venta_info)
        etiqueta_cliente.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def mostrar_clientes():
    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Estos son los clientes actuales:",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    cursor.execute("SELECT * FROM Clientes")
    clientes_info = cursor.fetchall()

    etiqueta_clientes = tkinter.Label(ventana3, text="Información de Clientes:")
    etiqueta_clientes.pack()

    for cliente_info in clientes_info:
        etiqueta_cliente = tkinter.Label(ventana3, text=cliente_info)
        etiqueta_cliente.pack()

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def menu_de_usuarios():
    ventana4 = tkinter.Toplevel()
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

    boton6 = tkinter.Button(ventana4, text="Editar usuarios", command=edit_user, bg="green",
                            fg="black", width=15, height=2, bd=12)
    boton6.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def menu_de_clientes():
    ventana4 = tkinter.Toplevel()
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
    boton5 = tkinter.Button(ventana4, text="Editar clientes", command=edit_customer, bg="green", fg="black", width=15,
                            height=2, bd=12)
    boton5.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def menu_de_facturas():
    ventana4 = tkinter.Toplevel()
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


def compra():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def limpiar_datos_actualizados():
        etiqueta_nuevo_nombre.pack_forget()
        cuadro_nuevo_nombre.pack_forget()

    def verificar_cliente(nombre_cliente, nit_cliente, producto_seleccionados):
        try:
            cursor.execute("SELECT * FROM Clientes WHERE nombre = %s AND identificador = %s",
                           (nombre_cliente, nit_cliente))
            cliente_existente = cursor.fetchone()

            if not cliente_existente:
                respuesta = messagebox.askyesno("Cliente no encontrado",
                                                "El cliente no existe en la base de datos. ¿Desea agregarlo?")
                if respuesta:
                    cursor.execute("INSERT INTO Clientes (nombre, identificador) VALUES (%s, %s)",
                                   (nombre_cliente, nit_cliente))
                    conn.commit()

            generar_factura(nombre_cliente, nit_cliente, productos_seleccionados)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al verificar cliente y generar factura: {e}")

    def generar_factura(nombre_cliente, nit_cliente, productos_seleccionados):
        try:
            num_factura = random.randint(0, 100000)
            doc = SimpleDocTemplate(f"Factura_{num_factura}.pdf", pagesize=letter)

            # Crear un StyleSheet
            styles = getSampleStyleSheet()

            elementos = []

            # Agregar el logo al inicio de la factura
            logo_path = "30-AÑOS-AGREQUIMA.png"  # Ruta de la imagen del logo
            logo = Image(logo_path, width=200, height=100)  # Ajustar el tamaño de la imagen según sea necesario
            elementos.append(logo)

            contenido = [
                f"Cliente: {nombre_cliente}",
                f"NIT: {nit_cliente}",
                f"Número de Factura: {num_factura}"
            ]

            # Usar el estilo 'Normal' del StyleSheet para los Paragraph
            elementos.extend([Paragraph(line, styles['Normal']) for line in contenido])

            detalles_productos = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]
            total_factura = 0

            for num_producto, cantidad in productos_seleccionados:
                cursor.execute("SELECT nombre, precio FROM Productos WHERE num_producto = %s", (num_producto,))
                producto = cursor.fetchone()

                if producto:
                    nombre_producto = producto[0]
                    precio_producto = producto[1]
                    subtotal_producto = cantidad * precio_producto
                    detalles_productos.append(
                        [nombre_producto, str(cantidad), f"Q{precio_producto:.2f}", f"Q{subtotal_producto:.2f}"])
                    total_factura += subtotal_producto

            tabla_productos = Table(detalles_productos)
            # Definir el estilo de la tabla correctamente
            estilo_tabla = TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Borde interno
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)  # Borde externo
            ])
            tabla_productos.setStyle(estilo_tabla)
            elementos.append(tabla_productos)

            elementos.append(Paragraph(f"Total: Q{total_factura:.2f}", styles['Heading1']))  # Ejemplo de otro estilo

            doc.build(elementos)

            messagebox.showinfo("¡ÉXITO!", f"Factura generada exitosamente: Factura_{num_factura}.pdf")

            # Guardar factura en la base de datos
            cursor.execute("INSERT INTO Factura (num_factura, nombre, tel, cantidad) VALUES (%s, %s, %s, %s)",
                           (num_factura, nombre_cliente, nit_cliente, len(productos_seleccionados)))
            conn.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al generar la factura: {e}")

    def obtener_datos():
        num_producto = cuadro_de_compra.get().strip()

        try:
            num_producto = int(num_producto)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número de producto válido.")
            return

        consulta = "SELECT * FROM Productos WHERE num_producto = %s"
        cursor.execute(consulta, (num_producto,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Producto no encontrado.")
        else:
            global boton_si, boton_no, etiqueta_de_eliminacion
            etiqueta_de_eliminacion = tkinter.Label(ventana4,
                                                    text=f"Producto encontrado:\n{registro[1]} - Stock: {registro[2]}\nDesea comprar este producto? Si / No")
            etiqueta_de_eliminacion.pack(pady=10)

            def boton_si():
                limpiar_datos()
                cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad a comprar", initialvalue=1)

                try:
                    if cantidad and cantidad > 0:
                        cursor.execute("SELECT * FROM Productos WHERE num_producto = %s", (num_producto,))
                        producto = cursor.fetchone()

                        if not producto:
                            messagebox.showerror("Error", "Producto no encontrado.")
                        else:
                            if cantidad <= producto[2]:
                                productos_seleccionados.append((num_producto, cantidad))
                                messagebox.showinfo("Éxito", "Producto agregado al carrito.")
                                nueva_cantidad = producto[2] - cantidad
                                cursor.execute("UPDATE Productos SET stock = %s WHERE num_producto = %s",
                                               (nueva_cantidad, num_producto))
                                conn.commit()
                            else:
                                messagebox.showerror("Error", "No hay suficiente stock para esta compra.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al buscar o actualizar producto: {e}")

            def boton_no():
                limpiar_datos()

            boton_si = tkinter.Button(ventana4, text="Si", command=boton_si, bg="blue", fg="white", width=15, height=2,
                                      bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana4, text="No", command=boton_no, bg="blue", fg="white", width=15, height=2,
                                      bd=12)
            boton_no.pack(pady=10)

    def finalizar_compra():
        if not productos_seleccionados:
            messagebox.showwarning("Advertencia", "No ha seleccionado ningún producto.")
        else:
            nombre_cliente = simpledialog.askstring("Cliente", "Ingrese su nombre:")
            nit_cliente = simpledialog.askinteger("Cliente", "Ingrese su NIT:")
            if nombre_cliente and nit_cliente:
                verificar_cliente(nombre_cliente, nit_cliente, productos_seleccionados)

    ventana4 = tkinter.Tk()
    ventana4.geometry("700x700")

    etiqueta_compra = tkinter.Label(ventana4, text="Por favor ingrese el número de su producto a comprar",
                                    font=("times new roman", 14))
    etiqueta_compra.pack(pady=20)

    cuadro_de_compra = tkinter.Entry(ventana4, font=("times new roman", 12))
    cuadro_de_compra.pack(pady=10)

    boton_obtener_datos = tkinter.Button(ventana4, text="Obtener Datos", command=obtener_datos,
                                         bg="blue", fg="white", width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    boton_finalizar_compra = tkinter.Button(ventana4, text="Finalizar Compra", command=finalizar_compra,
                                            bg="green", fg="white", width=15, height=2, bd=12)
    boton_finalizar_compra.pack(pady=10)

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=ventana4.destroy,
                                    bg="red", fg="white", width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)
    ventana4.mainloop()


def ver_productos():
    ventana4 = tkinter.Toplevel()
    ventana4.geometry("700x700")
    etiqueta_productos = tkinter.Label(ventana4, text="Productos actuales:",
                                       font=("times new roman", 14))
    etiqueta_productos.pack(pady=20)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    cursor.execute("SELECT * FROM Productos")
    productos_info = cursor.fetchall()

    for productos_info in productos_info:
        etiqueta_prodcuto = tkinter.Label(ventana4, text=productos_info)
        etiqueta_prodcuto.pack()

    def regresar1():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def agregar_producto():
    global conn, cursor

    def obtener_datos():
        global conn, cursor
        num_del_producto = cuadro_nombre.get()
        nombre = cuadro_contrasenia.get()
        stock = cuadro_ID.get()
        precio = cuadro_precio.get()

        if not num_del_producto:
            messagebox.showerror("Error", "Por favor, ingresa un número válido (número entero).")
            return
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return
        if not stock:
            messagebox.showerror("Error", "Por favor, ingresa un número de cantidad (stock) válido (número entero).")
        if not precio:
            messagebox.showerror("Error", "Por favor, ingresa un número de valor válido.")
        try:
            nombre = str(nombre)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
        try:
            num_del_producto = int(num_del_producto)
        except:
            messagebox.showerror("Error", "Por favor, número válido (número entero).")
        try:
            stock = int(stock)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un número de cantidad (stock) válido (número entero).")
        try:
            precio = int(precio) or float(precio)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un número de valor válido.")

        consulta = "SELECT * FROM Productos WHERE num_producto = %s"
        cursor.execute(consulta, (num_del_producto,))
        registro = cursor.fetchone()
        if registro:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido (número entero).")
        elif not registro:
            cursor = conn.cursor()
            cursor.execute(" INSERT INTO Productos(num_producto, nombre, stock, precio) VALUES (%s, %s, %s, %s)",
                           (num_del_producto, nombre, stock, precio))

            conn.commit()
            messagebox.showinfo("¡EXITO!", "Su producto fue agregado correctamente")
        else:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido (número entero).")

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el número del producto, nombre, stock, precio de su nuevo "
                                             "produto: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)
    etiqueta_nombre = tkinter.Label(ventana3, text="Número del producto:", font=("times new roman", 12))
    etiqueta_nombre.pack()
    cuadro_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_nombre.pack(pady=10)
    etiqueta_contrasenia = tkinter.Label(ventana3, text="Nombre del producto:", font=("times new roman", 12))
    etiqueta_contrasenia.pack()
    cuadro_contrasenia = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_contrasenia.pack(pady=10)
    etiqueta_ID = tkinter.Label(ventana3, text="Stock:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_ID = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_ID.pack(pady=10)
    etiqueta_precio = tkinter.Label(ventana3, text="Precio del producto", font=("times new roman", 12))
    etiqueta_precio.pack(pady=10)
    cuadro_precio = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_precio.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Obtener Datos", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def editar_producto():
    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def limpiar_datos_actualizados():
        etiqueta_nuevo_nombre.pack_forget()
        cuadro_nuevo_nombre.pack_forget()
        etiqueta_nuevo_cel.pack_forget()
        cuadro_nuevo_cel.pack_forget()
        etiqueta_nuevo_nit.pack_forget()
        cuadro_nuevo_nit.pack_forget()
        boton_aceptar.pack_forget()

    def actualizar_datos(num_producto, nuevo_nombre, nuevo_telefono, nuevo_nit):
        if not nuevo_nombre:
            messagebox.showerror("Error", "Por favor, ingresa un nombre válido.")
            return

        try:
            nuevo_telefono = int(nuevo_telefono)
            if nuevo_telefono < 0:
                raise ValueError("Stock debe ser un número positivo.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número de stock válido (número entero positivo).")
            return

        try:
            nuevo_nit = float(nuevo_nit)
            if nuevo_nit < 0:
                raise ValueError("Precio debe ser un número positivo.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un precio válido (número positivo).")
            return

        cursor.execute("UPDATE Productos SET nombre = %s, stock = %s, precio = %s WHERE num_producto = %s",
                       (nuevo_nombre, nuevo_telefono, nuevo_nit, num_producto))

        conn.commit()
        messagebox.showinfo("¡ÉXITO!", "¡Producto actualizado correctamente!")
        limpiar_datos_actualizados()

    def obtener_datos():
        num_producto = cuadro_num_producto.get()

        if not num_producto:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido (número entero).")
            return
        try:
            num_producto = int(num_producto)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido (número entero).")
            return

        consulta = "SELECT * FROM Productos WHERE num_producto = %s"
        cursor.execute(consulta, (num_producto,))
        registro = cursor.fetchone()

        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Producto encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea editar este producto ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                limpiar_datos()
                global etiqueta_nuevo_nombre, cuadro_nuevo_nombre, etiqueta_nuevo_cel, cuadro_nuevo_cel, etiqueta_nuevo_nit, cuadro_nuevo_nit, boton_aceptar
                etiqueta_nuevo_nombre = tkinter.Label(ventana3, text="Ingrese el nuevo nombre: ",
                                                      font=("times new roman", 12))
                etiqueta_nuevo_nombre.pack()
                cuadro_nuevo_nombre = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nombre.pack(pady=10)
                etiqueta_nuevo_cel = tkinter.Label(ventana3, text="Ingrese el nuevo número de stock de su producto: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_cel.pack()
                cuadro_nuevo_cel = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_cel.pack(pady=10)
                etiqueta_nuevo_nit = tkinter.Label(ventana3, text="Ingrese el nuevo precio de su producto: ",
                                                   font=("times new roman", 12))
                etiqueta_nuevo_nit.pack()
                cuadro_nuevo_nit = tkinter.Entry(ventana3, font=("times new roman", 12))
                cuadro_nuevo_nit.pack(pady=10)

                boton_aceptar = tkinter.Button(ventana3, text="Aceptar",
                                               command=lambda: actualizar_datos(num_producto,
                                                                                cuadro_nuevo_nombre.get(),
                                                                                cuadro_nuevo_cel.get(),
                                                                                cuadro_nuevo_nit.get()),
                                               bg="blue", fg="white", width=15, height=2, bd=12)
                boton_aceptar.pack(pady=10)

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un número de producto válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su producto no fue editado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el Número del producto que desea editar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="No. del producto:", font=("times new roman", 12))
    etiqueta_ID.pack()
    cuadro_num_producto = tkinter.Entry(ventana3, font=("times new roman", 12))
    cuadro_num_producto.pack(pady=10)
    boton_obtener_datos = tkinter.Button(ventana3, text="Aceptar", command=obtener_datos, bg="blue", fg="white",
                                         width=15, height=2, bd=12)
    boton_obtener_datos.pack(pady=10)

    def regresar1():
        ventana3.destroy()

    boton_regresar = tkinter.Button(ventana3, text="Regresar al menú", command=regresar1, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def eliminar_producto():
    global conn, cursor

    def limpiar_datos():
        etiqueta_de_eliminacion.pack_forget()
        boton_si.pack_forget()
        boton_no.pack_forget()

    def obtener_datos():
        num_producto = cuadro_ID.get()
        try:
            num_producto = int(num_producto)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto  válido.")

        consulta = "SELECT * FROM Productos WHERE num_producto = %s"
        cursor.execute(consulta, (num_producto,))
        registro = cursor.fetchone()
        if not registro:
            messagebox.showerror("Error", "Por favor, ingresa un número de producto válido.")
        else:
            global etiqueta_de_eliminacion, boton_si, boton_no
            etiqueta_de_eliminacion = tkinter.Label(ventana3, text="Usuario encontrado:\n"
                                                                   f"{registro}\n"
                                                                   f"Desea eliminar al usuario ? Si / No")
            etiqueta_de_eliminacion.pack()

            def boton_si():
                cursor.execute("DELETE FROM Productos WHERE num_producto = %s", (num_producto,))
                conn.commit()
                messagebox.showinfo("¡EXITO!", "Su producto fue eliminado correctamente")
                limpiar_datos()

            def boton_no():
                if not registro:
                    messagebox.showerror("Error", "Por favor, ingresa un número de producto válido.")
                else:
                    messagebox.showinfo("¡EXITO!", "Su producto no fue eliminado")
                    limpiar_datos()

            boton_si = tkinter.Button(ventana3, text="Si", command=boton_si, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_si.pack(pady=10)
            boton_no = tkinter.Button(ventana3, text="No", command=boton_no, bg="blue", fg="white", width=15,
                                      height=2, bd=12)
            boton_no.pack(pady=10)

    ventana3 = tkinter.Toplevel()
    ventana3.geometry("700x700")
    etiqueta3 = tkinter.Label(ventana3, text="Ingrese el número del producto que desea eliminar: ",
                              font=("times new roman", 14))
    etiqueta3.pack(pady=20)

    etiqueta_ID = tkinter.Label(ventana3, text="No. del producto:", font=("times new roman", 12))
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


def menu_de_productos():
    ventana4 = tkinter.Toplevel()
    ventana4.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana4, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana4, text="Ver productos", command=ver_productos, bg="lime",
                            fg="black", width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana4, text="Hacer una compra", command=compra, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana4, text="Agregar producto", command=agregar_producto, bg="lime", fg="black",
                            width=15, height=2, bd=12)
    boton4.pack(pady=5)
    boton5 = tkinter.Button(ventana4, text="Editar producto", command=editar_producto, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton5.pack(pady=5)
    boton6 = tkinter.Button(ventana4, text="Eliminar producto", command=eliminar_producto, bg="lime", fg="black",
                            width=15, height=2, bd=12)
    boton6.pack(pady=5)

    def regresar2():
        ventana4.destroy()

    boton_regresar = tkinter.Button(ventana4, text="Regresar al menú", command=regresar2, bg="red", fg="white",
                                    width=15, height=2, bd=12)
    boton_regresar.pack(pady=5)


def vermenu():
    ventana2 = tkinter.Toplevel()
    ventana2.geometry("700x700")
    etiqueta2 = tkinter.Label(ventana2, text="¿Qué desea hacer?", font=("times new roman", 14))
    etiqueta2.pack(pady=20)
    boton2 = tkinter.Button(ventana2, text="Ver menú de usuarios", command=menu_de_usuarios, bg="green", fg="black",
                            width=15, height=2, bd=12)
    boton2.pack(pady=5)
    boton3 = tkinter.Button(ventana2, text="Ver menú de clientes", command=menu_de_clientes, bg="orange", fg="white",
                            width=15, height=2, bd=12)
    boton3.pack(pady=5)
    boton4 = tkinter.Button(ventana2, text="Ver menú de facturas", command=menu_de_facturas, bg="violet", fg="white",
                            width=15, height=2, bd=12)
    boton4.pack(pady=5)
    boton5 = tkinter.Button(ventana2, text="Ver menú de productos", command=menu_de_productos, bg="navy", fg="white",
                            width=15, height=2, bd=12)
    boton5.pack(pady=5)

    boton_mostrar_tablas = tkinter.Button(ventana2, text="Mostrar Tablas", command=mostrar_tablas, bg="purple",
                                          fg="white", width=15, height=2, bd=12)
    boton_mostrar_tablas.pack(pady=5)

    def regresar():
        ventana2.destroy()

    boton_regresar = tkinter.Button(ventana2, text="Regresar al menú", command=regresar, bg="red", fg="white", width=15,
                                    height=2, bd=12)
    boton_regresar.pack(pady=5)


def salir():
    ventana.destroy()


def obtener_datos1():
    identificador = cuadro_login.get().strip()

    if not identificador:
        try:
            identificador = int(identificador)
        except:
            messagebox.showerror("Error", "Por favor, ingresa un ID válido.")

    def salir():
        ventana2.destroy()

    consulta = "SELECT * FROM Usuarios WHERE identificador = %s"
    cursor.execute(consulta, (identificador,))
    registro = cursor.fetchone()
    if not registro:
        messagebox.showerror("Error", "Por favor, ingresa un ID válido.")
    elif registro:
        ventana2 = tkinter.Toplevel()
        ventana2.geometry("900x700")
        etiqueta = tkinter.Label(ventana2, text="BIENVENIDO AL MENÚ",
                                 font=("times new roman", 14))
        etiqueta.pack(pady=20)
        a = (registro[1])
        etiqueta = tkinter.Label(ventana2, text=a,
                                 font=("times new roman", 14))
        etiqueta.pack(pady=20)

        boton0 = tkinter.Button(ventana2, text="Ver el menú", command=vermenu, font=("times new roman", 12),
                                bg="blue",
                                fg="white", width=15, height=2, bd=12)
        boton0.pack(pady=5)
        boton1 = tkinter.Button(ventana2, text="Salir", command=salir, font=("times new roman", 12), bg="red",
                                fg="black",
                                width=15, height=2, bd=12)
        boton1.pack(pady=5)
    else:
        messagebox.showerror("Error", "Por favor, ingresa un ID válido.")


etiqueta_login = tkinter.Label(ventana, text="Ingrese su ID por favor", font=("times new roman", 14))
etiqueta_login.pack(pady=20)
etiqueta_ID = tkinter.Label(ventana, text="ID:", font=("times new roman", 12))
etiqueta_ID.pack()
cuadro_login = tkinter.Entry(ventana, font=("times new roman", 12))
cuadro_login.pack(pady=10)
boton_obtener_datos = tkinter.Button(ventana, text="Aceptar", command=obtener_datos1, bg="blue", fg="white",
                                     width=15, height=2, bd=12)
boton_obtener_datos.pack(pady=10)
boton_salir = tkinter.Button(ventana, text="Salir", command=salir, bg="red", fg="white",
                             width=15, height=2, bd=12)
boton_salir.pack(pady=10)
ventana.mainloop()
