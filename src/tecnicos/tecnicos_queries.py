from database_connection import DatabaseConnection
from .tecnicos import Tecnico

def obtener_tecnicos():
    """Obtiene todos los tecnicos y los devuelve como una lista de objetos Tecnico."""
    db = DatabaseConnection()
    query = "SELECT ci, nombre, apellido, telefono FROM tecnicos ORDER BY apellido, nombre"
    rows = db.execute_query(query)
    db.close_connection()
    
    tecnicos: list[Tecnico] = []
    if rows:
        for row in rows:
            tecnicos.append(Tecnico(row['ci'], row['nombre'], row['apellido'], row['telefono']))
    return tecnicos

def obtener_tecnico_por_ci(ci_tecnico: str):
    """Obtiene un tecnico por su CI y lo devuelve como un objeto Tecnico."""
    db = DatabaseConnection()
    query = "SELECT ci, nombre, apellido, telefono FROM tecnicos WHERE ci = %s"
    row = db.execute_query(query, (ci_tecnico,))
    db.close_connection()
    
    if row:
        r = row[0]
        return Tecnico(r['ci'], r['nombre'], r['apellido'], r['telefono'])
    return None

def crear_tecnico(tecnico: Tecnico):
    """Crea un nuevo tecnico en la base de datos a partir de un objeto Tecnico."""
    db = DatabaseConnection()
    query = "INSERT INTO tecnicos (ci, nombre, apellido, telefono) VALUES (%s, %s, %s, %s)"
    params = (tecnico.ci, tecnico.nombre, tecnico.apellido, tecnico.telefono)
    db.execute_modification(query, params)
    db.close_connection()

def modificar_tecnico(tecnico: Tecnico):
    """Modifica los datos de un tecnico existente usando un objeto Tecnico."""
    db = DatabaseConnection()
    query = "UPDATE tecnicos SET nombre = %s, apellido = %s, telefono = %s WHERE ci = %s"
    params = (tecnico.nombre, tecnico.apellido, tecnico.telefono, tecnico.ci)
    db.execute_modification(query, params)
    db.close_connection()

def eliminar_tecnico(ci_tecnico: str):
    """Elimina un tecnico de la base de datos por su CI."""
    db = DatabaseConnection()
    query = "DELETE FROM tecnicos WHERE ci = %s"
    db.execute_modification(query, (ci_tecnico,))
    db.close_connection()

#5c. Consulta para reportes: Técnicos con más mantenimientos realizados.
def tecnicos_mas_mantenimientos():
    """Obtiene los tecnicos con más mantenimientos realizados."""
    db = DatabaseConnection()
    query = """
        SELECT t.ci, CONCAT(t.nombre, ' ', t.apellido) AS tecnico, COUNT(m.id) AS total_mantenimientos
        FROM tecnicos t
        LEFT JOIN mantenimientos m ON t.ci = m.ci_tecnico
        GROUP BY t.ci, t.nombre, t.apellido
        ORDER BY total_mantenimientos DESC
    """
    tecnicos_mas_mantenimientos = db.execute_query(query)
    db.close_connection()
    
    return tecnicos_mas_mantenimientos

