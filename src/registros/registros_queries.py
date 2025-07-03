from ..database_connection import DatabaseConnection
from .registros import Registro

def obtener_registros():
    """Obtiene todos los registros y los devuelve como una lista de objetos Registro."""
    db = DatabaseConnection()
    query = "SELECT id, id_maquina, id_insumo, fecha, cantidad_usada FROM registro_consumo ORDER BY fecha DESC"
    rows = db.execute_query(query)
    db.close_connection()

    registros: list[Registro] = []
    if rows:
        for row in rows:
            registros.append(Registro(row['id'], row['id_maquina'], row['id_insumo'], row['fecha'], row['cantidad_usada']))
    return registros

def obtener_registro_por_id(id_registro: int):
    """Obtiene un registro por su ID y lo devuelve como un objeto Registro."""
    db = DatabaseConnection()
    query = "SELECT id, id_maquina, id_insumo, fecha, cantidad_usada FROM registro_consumo WHERE id = %s"
    row = db.execute_query(query, (id_registro,))
    db.close_connection()

    if row:
        r = row[0]
        return Registro(r['id'], r['id_maquina'], r['id_insumo'], r['fecha'], r['cantidad_usada'])
    return None

def crear_registro(registro: Registro):
    """Crea un nuevo registro en la base de datos a partir de un objeto Registro."""
    db = DatabaseConnection()
    query = "INSERT INTO registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES (%s, %s, %s, %s)"
    params = (registro.id_maquina, registro.id_insumo, registro.fecha, registro.cantidad_usada)
    db.execute_modification(query, params)
    db.close_connection()

def modificar_registro(registro: Registro):
    """Modifica los datos de un registro existente usando un objeto Registro."""
    db = DatabaseConnection()
    query = "UPDATE registro_consumo SET id_maquina = %s, id_insumo = %s, fecha = %s, cantidad_usada = %s WHERE id = %s"
    params = (registro.id_maquina, registro.id_insumo, registro.fecha, registro.cantidad_usada, registro.id)
    db.execute_modification(query, params)
    db.close_connection()

def eliminar_registro(id_registro: int):
    """Elimina un registro de la base de datos por su ID."""
    db = DatabaseConnection()
    query = "DELETE FROM registro_consumo WHERE id = %s"
    db.execute_modification(query, (id_registro,))
    db.close_connection()

def calcular_costos_insumos_mensuales(año: int, mes: int):
    """Devuelve una lista de diccionarios con los costos totales de insumos por máquina en un mes específico."""
    db = DatabaseConnection()
    query = "SELECT rc.id_maquina, SUM(rc.cantidad_usada * i.precio_unitario) AS total_costo FROM registro_consumo rc JOIN insumos i ON rc.id_insumo = i.id WHERE YEAR(rc.fecha) = %s AND MONTH(rc.fecha) = %s GROUP BY rc.id_maquina "
    costos = db.execute_query(query, (año, mes))
    db.close_connection()
    return costos

def obtener_alquileres_mensuales():
    """Devuelve una lista de alquileres fijos por máquina y cliente."""
    db = DatabaseConnection()
    query = "SELECT m.id_cliente, m.id AS id_maquina, m.costo_alquiler_mensual FROM maquinas m WHERE m.id_cliente IS NOT NULL"
    alquileres = db.execute_query(query)
    db.close_connection()
    return alquileres
