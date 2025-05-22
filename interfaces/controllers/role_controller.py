from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.role_repository import RoleRepository
from utils.auth import role_required

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(role_required("super"))]
)


class RoleCreate(BaseModel):
    name: str
    state: bool

class RoleResponse(BaseModel):
    id_role: int
    name: str
    state: bool

@router.post("/", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    created_role = await repository.create_role(role)
    return RoleResponse(**created_role.__dict__)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    role = await repository.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return RoleResponse(**role.__dict__)

@router.get("/", response_model=List[RoleResponse])
async def get_all_roles(db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    roles = await repository.get_all_roles()
    return [RoleResponse(**role.__dict__) for role in roles]

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleCreate, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    updated_role = await repository.update_role(role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return RoleResponse(**updated_role.__dict__)

# No se elimina el rol, solo se cambia el estado a inactivo
@router.delete("/{role_id}", response_model=dict)
async def deactivate_role(role_id: int, db: AsyncSession = Depends(get_db)):
    repository = RoleRepository(db)
    await repository.delete_role(role_id)
    return {"detail": "Rol desactivado"}
