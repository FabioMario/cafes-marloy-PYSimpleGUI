from ..database_connection import DatabaseConnection
from .clientes import Cliente

def obtener_clientes():
    """Obtiene todos los clientes y los devuelve como una lista de objetos Cliente."""
    db = DatabaseConnection()
    query = "SELECT id, nombre, direccion, telefono, correo FROM clientes ORDER BY nombre"
    rows = db.execute_query(query)
    db.close_connection()
    
    clientes: list[Cliente] = []
    if rows:
        for row in rows:
            clientes.append(Cliente(row['id'], row['nombre'], row['direccion'], row['telefono'], row['correo']))
    return clientes

def obtener_cliente_por_id(id_cliente: int):
    """Obtiene un cliente por su ID y lo devuelve como un objeto Cliente."""
    db = DatabaseConnection()
    query = "SELECT id, nombre, direccion, telefono, correo FROM clientes WHERE id = %s"
    row = db.execute_query(query, (id_cliente,))
    db.close_connection()
    
    if row:
        r = row[0]
        return Cliente(r['id'], r['nombre'], r['direccion'], r['telefono'], r['correo'])
    return None

def crear_cliente(cliente: Cliente):
    """Crea un nuevo cliente en la base de datos a partir de un objeto Cliente."""
    db = DatabaseConnection()
    query = "INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES (%s, %s, %s, %s)"
    params = (cliente.nombre, cliente.direccion, cliente.telefono, cliente.correo)
    id_cliente = db.execute_modification(query, params)
    db.close_connection()
    return id_cliente

def modificar_cliente(cliente: Cliente):
    """Modifica los datos de un cliente existente usando un objeto Cliente."""
    db = DatabaseConnection()
    query = "UPDATE clientes SET nombre = %s, direccion = %s, telefono = %s, correo = %s WHERE id = %s"
    params = (cliente.nombre, cliente.direccion, cliente.telefono, cliente.correo, cliente.id)
    db.execute_modification(query, params)
    db.close_connection()

def eliminar_cliente(id_cliente: int):
    """Elimina un cliente de la base de datos por su ID."""
    db = DatabaseConnection()
    query = "DELETE FROM clientes WHERE id = %s"
    db.execute_modification(query, (id_cliente,))
    db.close_connection()