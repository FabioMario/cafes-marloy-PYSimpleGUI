import hashlib
import os
from cafes_marloy_app.database_connection import DatabaseConnection

salt_size = 64
hash_size = 64
iterations = 200000

def hash_password(password: str):
    """Hashea la contraseña con un salt aleatorio y la devuelve."""
    salt = os.urandom(salt_size)
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations, dklen=hash_size)
    return salt + key

def verify_password(email: str, password: str):
    """Verifica si la contraseña coincide con el hash almacenado para un correo."""
    db = DatabaseConnection()
    query = "SELECT correo, contraseña, es_administrador FROM login WHERE correo = %s"
    user_data = db.execute_query(query, (email,))
    db.close_connection()

    if user_data:
        user = user_data[0]
        hashed_password_from_db = user['contraseña']
        
        # Extraemos la sal del hash almacenado
        salt_from_db = hashed_password_from_db[:salt_size]
        
        # Hasheamos la contraseña ingresada con la misma sal
        new_key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt_from_db, iterations, dklen=hash_size)
        
        # Comparamos el hash completo
        if (salt_from_db + new_key) == hashed_password_from_db:
            return {'correo': user['correo'], 'es_administrador': user['es_administrador']}
            
    return None

def create_account(email: str, password: str, is_admin: bool = False):
    """Crea una nueva cuenta de usuario en la base de datos."""
    db = DatabaseConnection()
    
    # Primero, verificar si el correo ya existe
    check_query = "SELECT correo FROM login WHERE correo = %s"
    existing_user = db.execute_query(check_query, (email,))
    if existing_user:
        db.close_connection()
        return None # Indica que el usuario ya existe

    # Si no existe crea la cuenta
    hashed_password = hash_password(password)
    query = "INSERT INTO login (correo, contraseña, es_administrador) VALUES (%s, %s, %s)"
    params = (email, hashed_password, is_admin)
    
    user_id = db.execute_modification(query, params)
    db.close_connection()
    return user_id