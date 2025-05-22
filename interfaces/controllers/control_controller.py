from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.control_repository import ControlRepository
from application.use_case.manage_control import (
    create_control,
    get_control,
    get_all_controls,
    update_control,
    delete_control,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/controls",
    tags=["Controles"],
    dependencies=[Depends(role_required("admin"))]
)

class ControlCreate(BaseModel):
    control_type_id: int
    description: str
    frequency: Optional[str] = None
    responsible_id: str

class ControlResponse(BaseModel):
    id_control: int
    control_type_id: int
    description: str
    frequency: Optional[str]
    responsible_id: str

@router.post("/", response_model=ControlResponse, status_code=201)
async def create_control_endpoint(control: ControlCreate, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    created = await create_control(control, repository)
    return ControlResponse(**created.model_dump())

@router.get("/{control_id}", response_model=ControlResponse)
async def read_control_endpoint(control_id: int, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    control = await get_control(control_id, repository)
    if not control:
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return ControlResponse(**control.model_dump())

@router.get("/", response_model=List[ControlResponse])
async def read_all_controls_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    controls = await get_all_controls(repository)
    return [ControlResponse(**c.model_dump()) for c in controls]

@router.put("/{control_id}", response_model=ControlResponse)
async def update_control_endpoint(control_id: int, control: ControlCreate, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    updated = await update_control(control_id, control, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Control no encontrado")
    return ControlResponse(**updated.model_dump())

@router.delete("/{control_id}", response_model=dict)
async def delete_control_endpoint(control_id: int, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    await delete_control(control_id, repository)
    return {"detail": "Control eliminado"}
