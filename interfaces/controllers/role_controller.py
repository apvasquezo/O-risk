from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.role_repository import RoleRepository

router = APIRouter()

class RoleCreate(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: int
    name: str

@router.post("/roles/", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    created_role = await repository.create_role(role)
    return RoleResponse(id=created_role.id, name=created_role.name)

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    role = await repository.get_role(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return RoleResponse(id=role.id, name=role.name)

@router.get("/roles/", response_model=List[RoleResponse])
async def read_roles(db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    roles = await repository.get_all_roles()
    return [RoleResponse(id=role.id, name=role.name) for role in roles]

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleCreate, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    updated_role = await repository.update_role(role_id, role)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return RoleResponse(id=updated_role.id, name=updated_role.name)

@router.delete("/roles/{role_id}", response_model=dict)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    await repository.delete_role(role_id)
    return {"detail": "Role deleted"}