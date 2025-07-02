from ..database_connection import DatabaseConnection
from .maquinas import Maquina

def obtener_maquinas():
    """Obtiene todas las maquinas y las devuelve como una lista de objetos Maquina."""
    db = DatabaseConnection()
    query = "SELECT id, modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual FROM maquinas ORDER BY modelo"
    rows = db.execute_query(query)
    db.close_connection()
    
    maquinas: list[Maquina] = []
    if rows:
        for row in rows:
            maquinas.append(Maquina(row['id'], row['modelo'], row['id_cliente'], row['ubicacion_cliente'], row['costo_alquiler_mensual']))
    return maquinas

def obtener_maquina_por_id(id_maquina: int):
    """Obtiene una maquina por su ID y la devuelve como un objeto Maquina."""
    db = DatabaseConnection()
    query = "SELECT id, modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual FROM maquinas WHERE id = %s"
    row = db.execute_query(query, (id_maquina,))
    db.close_connection()
    
    if row:
        r = row[0]
        return Maquina(r['id'], r['modelo'], r['id_cliente'], r['ubicacion_cliente'], r['costo_alquiler_mensual'])
    return None

def crear_maquina(maquina: Maquina):
    """Crea una nueva maquina en la base de datos a partir de un objeto Maquina."""
    db = DatabaseConnection()
    query = "INSERT INTO maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual) VALUES (%s, %s, %s, %s)"
    params = (maquina.modelo, maquina.id_cliente, maquina.ubicacion_cliente, maquina.costo_alquiler_mensual)
    id_maquina = db.execute_modification(query, params)
    db.close_connection()
    return id_maquina

def modificar_maquina(maquina: Maquina):
    """Modifica los datos de una maquina existente usando un objeto Maquina."""
    db = DatabaseConnection()
    query = "UPDATE maquinas SET modelo = %s, id_cliente = %s, ubicacion_cliente = %s, costo_alquiler_mensual = %s WHERE id = %s"
    params = (maquina.modelo, maquina.id_cliente, maquina.ubicacion_cliente, maquina.costo_alquiler_mensual, maquina.id)
    db.execute_modification(query, params)
    db.close_connection()

def eliminar_maquina(id_maquina: int):
    """Elimina una maquina de la base de datos por su ID."""
    db = DatabaseConnection()
    query = "DELETE FROM maquinas WHERE id = %s"
    db.execute_modification(query, (id_maquina,))
    db.close_connection()