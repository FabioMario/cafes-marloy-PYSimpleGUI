class Cliente:
    def __init__(self, id: int, nombre: str, direccion: str, telefono: str, correo: str):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"Cliente(ID: {self.id}, Nombre: {self.nombre}, Direccion: {self.direccion}, Telefono: {self.telefono}, Correo: {self.correo})"
