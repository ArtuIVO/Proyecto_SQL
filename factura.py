class Facturas:
    def __init__(self, monto: int):
        self.monto = monto

    def __str__(self):
        return f"El monto es:{self.monto}"
