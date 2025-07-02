class Maquina:
    def __init__(self, id: int, modelo: str, id_cliente: int, ubicacion_cliente: str, costo_alquiler_mensual: float):
        self.id = id
        self.modelo = modelo
        self.id_cliente = id_cliente
        self.ubicacion_cliente = ubicacion_cliente
        self.costo_alquiler_mensual = costo_alquiler_mensual

    def __str__(self):
        return f"Maquina(ID: {self.id}, Modelo: {self.modelo}, ID Cliente: {self.id_cliente}, Ubicacion: {self.ubicacion_cliente}, Costo Alquiler: {self.costo_alquiler_mensual})"