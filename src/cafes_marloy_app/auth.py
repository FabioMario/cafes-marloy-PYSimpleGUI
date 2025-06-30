import hashlib
import os

salt_size = 64
hash_size = 64
iterations = 200000 #cuantas veces se hashea la contraseña

def hash_password(password):
    """Hashea la contraseña con un salt aleatorio y la devuelve."""
    salt = os.urandom(salt_size)
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations, dklen=hash_size)
    return salt + key

def verify_password(password, hashed_password):
    """Verifica la contraseña contra su version hasheada."""
    salt = hashed_password[:salt_size]
    new_key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations, dklen=hash_size)
    return salt + new_key == hashed_password
