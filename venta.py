class Factura:
    def __init__(self, nombre: str, tel:int, cantidad: int,  num_factura: int ):
        self.nombre = nombre
        self.tel = tel
        self.cantidad = cantidad
        self.num_factura = num_factura

    def __str__(self):
        return (f"Nombre del cliente: {self.nombre}"
                f"Número de telefono: {self.tel}"
                f"Cantidad del producto comprado: {self.cantidad}"
                f"No. de la factura: {self.num_factura}")