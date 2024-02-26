from usuario import Usuarios
from cliente import Cliente


class Node:
    def __init__(self, data: Usuarios | Cliente):
        self.data = data
        self.next: Node | None = None

    def __str__(self):
        return str(self.data)
