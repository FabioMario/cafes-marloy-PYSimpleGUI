from .insumos import Insumos
from database_connection import DatabaseConnection


def obtener_insumos():
    "Obtiene todos los insumos y los devuelve como una lista de objetos Insumos."
    db = DatabaseConnection()
    query = "SELECT id,descripcion,tipo,precio_unitario,id_proveedor FROM insumos ORDER BY id"
    rows = db.execute_query(query)
    db.close_connection()

    insumos: list[Insumos] = []
    if rows:
        for row in rows:
            insumos.append(Insumos(row['id'],row['descripcion'],row['tipo'],row['precio_unitario'],row['id_proveedor']))
    return insumos

def obtener_insumo_por_id(id_insumo: int):
    """Obtiene un insumo por su ID y lo devuelve como un objeto Insumo."""
    db = DatabaseConnection()
    query = "SELECT id,descripcion,tipo,precio_unitario,id_proveedor FROM insumos WHERE id = %s"
    row = db.execute_query(query, (id_insumo,))
    db.close_connection()
    if row:
        r=row[0]
        return Insumos(r['id'],r['descripcion'],r['tipo'],r['precio_unitario'],r['id_proveedor'])
    return None

def obtener_insumos_por_id_proveedor(id_proveedor: int):
    """Obtiene todos los insumos de un proveedor y los devuelve como una lista de objetos Insumo."""
    db = DatabaseConnection()
    query = "SELECT id,descripcion,tipo,precio_unitario,id_proveedor FROM insumos WHERE id_proveedor = %s"
    rows = db.execute_query(query, (id_proveedor,))
    db.close_connection()
    
    insumos: list[Insumos] = []
    if rows:
        for row in rows:
            insumos.append(Insumos(row['id'], row['descripcion'], row['tipo'], row['precio_unitario'], row['id_proveedor']))
    return insumos

def crear_insumo(insumo: Insumos):
    """Crea un nuevo insumo en la base de datos a partir de un objeto Insumo"""
    db = DatabaseConnection()
    query = "INSERT INTO insumos (descripcion,tipo,precio_unitario,id_proveedor) VALUES (%s, %s, %s, %s)"
    params = (insumo.descripcion, insumo.tipo, insumo.precio_unitario, insumo.id_proveedor)
    id_insumo = db.execute_modification(query, params)
    db.close_connection()
    return id_insumo

def eliminar_insumo(id_insumo: int):
    """Elimina un insumo de la base de dato por su ID"""
    db = DatabaseConnection()
    query = "DELETE FROM insumos WHERE id = %s"
    db.execute_modification(query, (id_insumo,))
    db.close_connection()

def modificar_insumo(insumo: Insumos):
    """Modifica los datos de un insumo existente usando un objeto Insumo."""
    db = DatabaseConnection()
    query = "UPDATE insumos SET descripcion = %s, tipo = %s, precio_unitario = %s, id_proveedor = %s WHERE id = %s"
    params = (insumo.descripcion, insumo.tipo, insumo.precio_unitario, insumo.id_proveedor, insumo.id)
    db.execute_modification(query, params)
    db.close_connection()

#5b. Consultas para reportes: Insumos con mayor consumo y costo.
def generar_reporte_consumo_costo_insumos():
    """
    Genera un reporte de consumo y costo de insumos, ordenado por el costo total.
    """
    db = DatabaseConnection()
    
    query = """
        SELECT
            i.id AS id_insumo,
            i.descripcion,
            i.tipo,
            COALESCE(SUM(rc.cantidad_usada), 0) AS total_cantidad_consumida,
            COALESCE(SUM(rc.cantidad_usada * i.precio_unitario), 0) AS costo_total
        FROM
            insumos i
        LEFT JOIN
            registro_consumo rc ON i.id = rc.id_insumo
        GROUP BY
            i.id, i.descripcion, i.tipo
        ORDER BY
            costo_total DESC, total_cantidad_consumida DESC;
    """
    
    reporte = db.execute_query(query)
    db.close_connection()
    return reporte
