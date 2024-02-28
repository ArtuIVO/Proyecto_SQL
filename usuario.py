class Usuarios:
    def __init__(self, nombre: str, contrasenia: str, identificador: int):
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.identificador = identificador

    def __str__(self):
        return (f"Nombre del usuario: {self.nombre}\n"
                f"El ID del usurio: {self.identificador}\n")
