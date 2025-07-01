import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseConnection:
    """Establece una conexión para realizar operaciones en la base de datos."""
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        self.connection = None
        try:
            # Usar la configuración en config.py
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Conexión a la base de datos establecida.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def execute_query(self, query, params=None):
        """Ejecuta una consulta de tipo SELECT."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()

    def execute_modification(self, query, params=None):
        """Ejecuta una consulta de tipo INSERT, UPDATE, o DELETE."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            print("Modificación ejecutada con éxito.")
            return cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Error al ejecutar la modificación: {e}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada.")