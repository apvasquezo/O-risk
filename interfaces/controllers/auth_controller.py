from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from domain.repositories.user_repository import UserRepository
from application.use_case.manage_user import get_user_username
from infrastructure.database.db_config import get_db
from utils.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str  

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    db_user = await get_user_username(user.username, repository)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Mapea role_id a nombre legible
    role_map = {1: "super", 2: "admin"}
    role = role_map.get(db_user.role_id)
    print("role ", role)
    if not role:
        raise HTTPException(status_code=403, detail="Rol no autorizado")

    # Crea el token JWT con rol
    token = create_access_token({
        "sub": db_user.username,
        "role": role
    })
    print ("token ", token)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }