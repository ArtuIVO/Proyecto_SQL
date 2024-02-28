class Cliente:
    def __init__(self, nombre: str, identificador: int, cel: int):
        self.nombre = nombre
        self.identificador = identificador
        self.celular = cel

    def __str__(self):
        return (f"El cliente se llama: {self.nombre}\n"
                f"ID del cliente es: {self.identificador}\n"
                f"El número telefonico es: {self.celular}")
