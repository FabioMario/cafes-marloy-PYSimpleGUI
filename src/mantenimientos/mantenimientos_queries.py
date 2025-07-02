from ..database_connection import DatabaseConnection
from .mantenimientos import Mantenimiento


def obtener_mantenimiento():
    """Obtiene todos los mantenimientos y los devuelve como una lista de objetos mantenimiento"""
    db = DatabaseConnection()
    query = "SELECT id, id_maquina, ci_tecnico, fecha, tipo, observaciones FROM mantenimientos ORDER BY id"
    rows = db.get.execute_query(query)
    db.close_connection()
    mantenimientos: list[Mantenimiento] = []
    if rows:
        for row in rows:
            mantenimientos.append(Mantenimiento(row['id'], row['id_maquina'], row['ci_tecnico'], row['tipo'], row['observaciones']))
        return mantenimientos

def obtener_mantenimiento_por_id(id_mantenimiento: int):
    """"Obtiene un mantenimiento por su ID y lo devuelve como un objeto Mantenimiento"""
    db = DatabaseConnection()
    query = "SELECT id, id_maquina, ci_tecnico, fecha, tipo, observaciones FROM mantenimientos WHERE id=%s"
    row = db.execute_query(query, (id_mantenimiento,))
    if row:
        r=row[0]
        return Mantenimiento(r['id'], r['id_maquina'], r['ci_tecnico'], r['tipo'], r['observaciones'])
    return None

def crear_mantenimiento(mante: Mantenimiento):
    """Crea un nuevo mantenimiento en la base de dato a partir de un objeto Mantenimiento"""
    db = DatabaseConnection()
    query = "INSERT INTO mantenimientos(id_maquina, ci_tecnico, fecha, tipo, observaciones) VALUES (%s, %s, %s, %s, %s)"
    params = (mante.id_maquina, mante.ci_tecnico, mante.fecha, mante.tipo, mante.observaciones)
    id_mantenimiento = db.execute_modification(query, params)
    db.close_connection()
    return id_mantenimiento

def eliminar_mantenimiento(id_mantenimiento: Mantenimiento):
    """"Elimina un mantenimiento de la base de dato por su ID"""
    db = DatabaseConnection()
    query = "DELETE FROM mantenimientos WHERE id = %s"
    db.execute_query(query, (id_mantenimiento,))
    db.close_connection()