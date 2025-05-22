from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import create_access_token
from domain.repositories.user_repository import UserRepository
from application.use_case.manage_user import get_user_username
from infrastructure.database.db_config import get_db
from utils.auth import verify_password, create_access_token, decode_token, role_required

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role_id:int
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    print("usuario ", user)
    # Instancia del repositorio
    repository = UserRepository(db)

    # Obtener usuario por username
    print("username ", user.username)
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
    token = create_access_token({"sub": db_user.username, "role": db_user.role_id})
    print("Authentication successful.")
    print ("token ", token)
    print("role ", db_user.role_id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role_id": db_user.role_id  # Agregar este campo
    }