class Factura:
    def __init__(self, nombre: str, nit: int, cantidad: int, num_factura: int):
        self.nombre = nombre
        self.nit = nit
        self.cantidad = cantidad
        self.num_factura = num_factura

    def __str__(self):
        return (f"Nombre del cliente: {self.nombre}\n"
                f"Número de nit: {self.nit}\n"
                f"Cantidad del producto comprado: {self.cantidad}\n"
                f"No. de la factura: {self.num_factura}\n")
