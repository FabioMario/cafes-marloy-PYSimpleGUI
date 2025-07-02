class Tecnico:
    def __init__(self, ci: str, nombre: str, apellido: str, telefono: str):
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def __str__(self):
        return f"Tecnico(CI: {self.ci}, Nombre: {self.nombre}, Apellido: {self.apellido}, Telefono: {self.telefono})"