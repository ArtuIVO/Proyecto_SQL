from comida import
from usuario import
from factura import Facturas


class Node:
    def __init__(self, data: Comida | Clientes | Facturas):
        self.data = data
        self.next: Node | None = None

    def __str__(self):
        return str(self.data)
