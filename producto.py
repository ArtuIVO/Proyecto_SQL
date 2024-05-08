class Producto:
    def __init__(self, num_de_producto: int, nombre: str, stock: int, precio: float):
        self.nombre = nombre
        self.stock = stock
        self.precio = precio
        self.num_producto = num_de_producto

    def __str__(self):
        return (f"ID: {self.num_producto}\n"
                f"Nombre del curso: {self.nombre}\n"
                f"Cantindad del cursos disponibles: {self.stock}\n"
                f"Precio del producto: Q{self.precio}\n")