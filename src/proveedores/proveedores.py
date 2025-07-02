class Proveedor:
    def __init__(self, id: int, nombre: str, contacto: str):
        self.id = id
        self.nombre = nombre
        self.contacto = contacto
    def __str__(self):
        return f"Proveedor: (ID: {self.id}, Nombre: {self.nombre}, Contacto: {self.contacto})"