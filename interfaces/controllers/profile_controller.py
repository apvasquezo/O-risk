from fastapi import APIRouter, Depends
from utils.auth import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from fastapi import Body

router = APIRouter(
    prefix="/api/profile", 
    tags=["profile"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/me")
async def get_profile_me(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    username = payload.get("sub")
    rol=payload.get("role")
    return {
        "username": username,
        "role": rol
    }

@router.put("/me")
async def update_profile_me(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
    data: dict = Body(...)
    ):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    username = payload.get("sub")
    repo = UserRepository(session)
    user = await repo.get_user_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    new_username = data.get("username")
    new_password = data.get("new_password")
    if new_username:
        user.username = new_username
    if new_password:
        user.password = new_password

    await repo.update_user(user.id_user, user)
    return {"message": "Perfil actualizado correctamente"}