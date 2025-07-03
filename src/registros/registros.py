import datetime


class Registro:
   def __init__(self,id: int, id_maquina: int, id_insumo: int, fecha: datetime, cantidad_usada: int):
       self.id = id
       self.id_maquina = id_maquina
       self.id_insumo = id_insumo
       self.fecha = fecha
       self.cantidad_usada = cantidad_usada

       def __str__(self):
        return f"Registro(ID: {self.id}, ID Maquina: {self.id_maquina}, ID Insumo: {self.id_insumo}, Fecha: {self.fecha}, Cantidad Usada: {self.cantidad_usada})"
