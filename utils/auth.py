import jwt
import hashlib
from datetime import datetime, timedelta

# Configuración para JWT
SECRET_KEY = "tu_secreto_super_seguro"  # Cambia esto por una clave secreta más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Función para hashear una contraseña usando SHA-256
def hash_password(password: str) -> str:
    """Hashea una contraseña usando SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Función para verificar una contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(f"Plain password: {plain_password}")
    print(f"Hashed password: {hashed_password}")
    result = plain_password == hashed_password
    print(f"Password match result: {result}")
    return result

# Función para crear un token de acceso
def create_access_token(data: dict) -> str:
    """Crea un token JWT con una expiración predeterminada."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para decodificar un token
def decode_token(token: str) -> dict | None:
    """Decodifica un token JWT y verifica su validez."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Error: El token ha expirado.")
        return None
    except jwt.PyJWTError:
        print("Error: Token inválido.")
        return None