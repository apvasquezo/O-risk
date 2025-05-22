from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.user_repository import UserRepository
from utils.auth import role_required
from application.use_case.manage_user import (
    create_user,
    get_user as get_user_use_case,
    get_all_users as get_all_users_use_case,
    update_user as update_user_use_case,
    delete_user as delete_user_use_case,
)

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
    dependencies=[Depends(role_required("super"))]
)

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int

class UserResponse(BaseModel):
    id_user: int
    username: str
    role_id: int

@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    created_user = await create_user(user.username, user.password, user.role_id, repository)
    return UserResponse(**created_user.__dict__)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    user = await get_user_use_case(user_id, repository)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse(**user.__dict__)

@router.get("/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    users = await get_all_users_use_case(repository)
    return [UserResponse(**user.__dict__) for user in users]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    updated_user = await update_user_use_case(user_id, user, repository)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse(**updated_user.__dict__)

@router.delete("/{user_id}", response_model=dict)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    await delete_user_use_case(user_id, repository)
    return {"detail": "Usuario eliminado"}
