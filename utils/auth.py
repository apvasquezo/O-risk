import jwt
import hashlib
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


# Configuración para JWT
SECRET_KEY = "tu_secreto_super_seguro"  # Cambia esto por una clave secreta más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    """Decodifica un token JWT y verifica su validez, incluyendo roles."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("decodificar ", payload)
        return payload  # payload debe incluir "role" y otros datos
    except jwt.ExpiredSignatureError:
        print("Error: El token ha expirado.")
        return None
    except jwt.PyJWTError:
        print("Error: Token inválido.")
        return None
   
def role_required(required_role: str):
    def role_dependency(token: str = Depends(oauth2_scheme)):
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user_role = payload.get("role")
        if user_role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return payload
    return role_dependency