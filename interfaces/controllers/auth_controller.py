from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from domain.repositories.user_repository import UserRepository
from application.use_case.manage_user import get_user_username
from infrastructure.database.db_config import get_async_session
from utils.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# Ruta principal para frontend (JSON)
@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    repository = UserRepository(db)
    db_user = await get_user_username(user.username, repository)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    role_map = {1: "super", 2: "admin"}
    role = role_map.get(db_user.role_id)
    if not role:
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    token = create_access_token({
        "sub": db_user.username,
        "role": role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }

# Ruta secundaria para pruebas desde Swagger (formulario)
@router.post("/login-docs", response_model=TokenResponse)
async def login_docs(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    repository = UserRepository(db)
    db_user = await get_user_username(form_data.username, repository)

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    role_map = {1: "super", 2: "admin"}
    role = role_map.get(db_user.role_id)
    if not role:
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    token = create_access_token({
        "sub": db_user.username,
        "role": role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }
