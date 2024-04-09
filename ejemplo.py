from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image


def generar_factura(nombre_cliente, numero_factura, productos, total):
    # Crear un lienzo (canvas) para el documento PDF
    pdf_filename = "factura.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Estilos de párrafo
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Heading1"]
    estilo_encabezado = estilos["Heading2"]
    estilo_normal = estilos["BodyText"]
    estilo_firma = ParagraphStyle(name="Firma", parent=estilo_normal, alignment=1)

    # Contenido de la factura
    contenido = []

    # Título
    titulo = Paragraph("Factura", estilo_titulo)
    contenido.append(titulo)

    # Imagen de la empresa
    imagen_empresa = Image("30-AÑOS-AGREQUIMA.png", width=150, height=50)
    imagen_empresa.drawHeight = 1.5 * inch * imagen_empresa.drawHeight / imagen_empresa.drawWidth
    imagen_empresa.drawWidth = 1.5 * inch
    contenido.append(imagen_empresa)

    # Información del cliente y número de factura
    contenido.append(Spacer(1, 20))
    contenido.append(Paragraph(f"<b>Cliente:</b> {nombre_cliente}", estilo_encabezado))
    contenido.append(Paragraph(f"<b>Número de Factura:</b> {numero_factura}", estilo_encabezado))
    contenido.append(Spacer(1, 10))

    # Lista de productos y precios
    data = [["Producto", "Precio"]]
    for producto, precio in productos.items():
        data.append([producto, f"${precio}"])

    tabla = Table(data)
    tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    contenido.append(tabla)

    # Total
    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph(f"<b>Total:</b> ${total}", estilo_encabezado))

    # Firma
    contenido.append(Spacer(1, 50))
    contenido.append(Paragraph("Firma ________________________", estilo_firma))

    # Generar el PDF
    doc.build(contenido)


# Ejemplo de uso
nombre_cliente = "Juan Perez"
numero_factura = "001"
productos = {"Producto 1": 20, "Producto 2": 30, "Producto 3": 15}
total = sum(productos.values())

generar_factura(nombre_cliente, numero_factura, productos, total)
