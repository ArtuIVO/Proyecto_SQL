class Producto:
    def __init__(self, nombre: str, stock: int, precio: int):
        self.nombre = nombre
        self.stock = stock
        self.precio = precio

    def __str__(self):
        return (f"Nombre del curso: {self.nombre}\n"
                f"Cantindad del cursos disponibles: {self.stock}\n"
                f"Precio del producto: Q{self.precio}\n")