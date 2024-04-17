class Producto:
    def __init__(self, nombre: str, stock: int, precio: int, num_de_producto: int):
        self.nombre = nombre
        self.stock = stock
        self.precio = precio
        self.num_producto = num_de_producto

    def __str__(self):
        return (f"ID: {self.num_producto}\n"
                f"Nombre del curso: {self.nombre}\n"
                f"Cantindad del cursos disponibles: {self.stock}\n"
                f"Precio del producto: Q{self.precio}\n")