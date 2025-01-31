from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.user_repository import UserRepository
from application.use_case.manage_user import (
    create_user,
    get_user_by_id,
    get_users,
    update_user,
    delete_user
)

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int

class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    created_user = await create_user(user, repository)
    return UserResponse(id=created_user.id, username=created_user.username, role_id=created_user.role_id)

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    user = await get_user_by_id(user_id, repository)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, username=user.username, role_id=user.role_id)

@router.get("/users/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    users = await get_users(repository)
    return [UserResponse(id=user.id, username=user.username, role_id=user.role_id) for user in users]

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    updated_user = await update_user(user_id, user, repository)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=updated_user.id, username=updated_user.username, role_id=updated_user.role_id)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repository = UserRepository(db)
    await delete_user(user_id, repository)
    return {"detail": "User deleted"}
