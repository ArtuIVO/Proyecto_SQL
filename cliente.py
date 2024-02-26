class Cliente():
    def __init__(self, nombre: str, identificador: int):
        self.nombre = nombre
        self.identificador = identificador

    def __str__(self):
        return (f"El cliente se llama: {self.nombre}"
                f"ID del cliente es: {self.identificador}")
