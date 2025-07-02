from datetime import datetime
class Mantenimiento:
        def __init__(self, id: int, id_maquina: int, ci_tecnico: str, tipo: int, fecha: datetime, observaciones: str):
            self.id = id
            self.id_maquina = id_maquina
            self.ci_tecnico = ci_tecnico
            self.tipo = tipo
            self.fecha = fecha
            self.observaciones = observaciones

        def __str__(self):
            return f"Mantenimiento: (ID: {self.id}, ID_maquina: {self.id_maquina}, CI_tecnico: {self.ci_tecnico}, Tipo: {self.tipo}, Fecha: {self.fecha}, Observaciones: {self.observaciones})"