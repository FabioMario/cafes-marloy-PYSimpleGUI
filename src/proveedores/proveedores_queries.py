from database_connection import DatabaseConnection
from .proveedores import Proveedor

def obtener_proveedores():
    """Obtiene todos los proveedores y los devuelve como una lista de objetos Proveedor."""
    db = DatabaseConnection()
    query = """
        SELECT
            id, 
            nombre, 
            contacto
        FROM
            proveedores
        ORDER BY
            nombre
    """
    rows = db.execute_query(query)
    db.close_connection()
    
    proveedores: list[Proveedor] = []
    if rows:
        for row in rows:
            proveedores.append(Proveedor(row['id'], row['nombre'], row['contacto']))
    return proveedores

def obtener_proveedor_por_id(id_proveedor: int):
    """Obtiene un proveedor por su ID y lo devuelve como un objeto Proveedor."""
    db = DatabaseConnection()
    query = """
        SELECT
            id, 
            nombre, 
            contacto
        FROM
            proveedores
        WHERE
            id = %s
    """
    row = db.execute_query(query, (id_proveedor,))
    db.close_connection()
    
    if row:
        r = row[0]
        return Proveedor(r['id'], r['nombre'], r['contacto'])
    return None

def crear_proveedor(proveedor: Proveedor):
    """Crea un nuevo proveedor en la base de datos a partir de un objeto Proveedor."""
    db = DatabaseConnection()
    query = """
        INSERT INTO proveedores (
            nombre, 
            contacto
        ) VALUES (
            %s, 
            %s
        )
    """
    params = (proveedor.nombre, proveedor.contacto)
    id_proveedor = db.execute_modification(query, params)
    db.close_connection()
    return id_proveedor

def modificar_proveedor(proveedor: Proveedor):
    """Modifica los datos de un proveedor existente usando un objeto Proveedor."""
    db = DatabaseConnection()
    query = """
        UPDATE
            proveedores
        SET
            nombre = %s, 
            contacto = %s
        WHERE
            id = %s
    """
    params = (proveedor.nombre, proveedor.contacto, proveedor.id)
    db.execute_modification(query, params)
    db.close_connection()

def eliminar_proveedor(id_proveedor: int):
    """Elimina un proveedor de la base de datos por su ID."""
    db = DatabaseConnection()
    query = """
        DELETE FROM
            proveedores
        WHERE
            id = %s
    """
    db.execute_modification(query, (id_proveedor,))
    db.close_connection()