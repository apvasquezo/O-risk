from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import create_access_token
from domain.repositories.user_repository import UserRepository
from application.use_case.manage_user import get_user_username
from infrastructure.database.db_config import get_db
from utils.auth import verify_password, create_access_token, decode_token

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Instancia del repositorio
    repository = UserRepository(db)

    # Obtener usuario por username
    db_user = await get_user_username(user.username, repository)

    # Verificar si el usuario existe
    if not db_user:
        print("User not found.")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Verificar si la contraseña es correcta
    if not verify_password(user.password, db_user.password):
        print("Password mismatch.")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Crear token de acceso
    token = create_access_token({"sub": db_user.username})
    print("Authentication successful.")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # Decodifica el token utilizando tu función personalizada
    payload = decode_token(token)
    if payload is None:  # Si el token no es válido o ha expirado
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username: str = payload.get("sub")
    if not username:  # Si el token no contiene un nombre de usuario válido
        raise HTTPException(status_code=401, detail="Invalid token")

    # Retorna el nombre de usuario del token
    return {"username": username}