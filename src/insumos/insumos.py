class Insumos:
    def __init__(self,id: int,descripcion: str,tipo: str,precio_unitario: int,id_proveedor: int):
        self.id = id
        self.descripcion = descripcion
        self.tipo = tipo
        self.precio_unitario = precio_unitario
        self.id_proveedor = id_proveedor
    def __str__(self):
        return f"Insumo(ID: {self.id},Descripcion{self.descripcion},Tipo {self.tipo},Precio {self.precio_unitario},ID_proveedor: {self.id_proveedor})"








