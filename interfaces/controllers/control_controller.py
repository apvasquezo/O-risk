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

router = APIRouter()

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

@router.post("/controls/", response_model=ControlResponse)
async def create_control_endpoint(control: ControlCreate, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    created_control = await create_control(control, repository)
    return ControlResponse(
        id_control=created_control.id_control,
        control_type_id=created_control.control_type_id,
        description=created_control.description,
        frequency=created_control.frequency,
        responsible_id=created_control.responsible_id
    )

@router.get("/controls/{control_id}", response_model=ControlResponse)
async def read_control_endpoint(control_id: int, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    control = await get_control(control_id, repository)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return ControlResponse(
        id_control=control.id_control,
        control_type_id=control.control_type_id,
        description=control.description,
        frequency=control.frequency,
        responsible_id=control.responsible_id
    )

@router.get("/controls/", response_model=List[ControlResponse])
async def read_all_controls_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    controls = await get_all_controls(repository)
    return [
        ControlResponse(
            id_control=c.id_control,
            control_type_id=c.control_type_id,
            description=c.description,
            frequency=c.frequency,
            responsible_id=c.responsible_id
        ) for c in controls
    ]

@router.put("/controls/{control_id}", response_model=ControlResponse)
async def update_control_endpoint(control_id: int, control: ControlCreate, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    updated_control = await update_control(control_id, control, repository)
    if not updated_control:
        raise HTTPException(status_code=404, detail="Control not found")
    return ControlResponse(
        id_control=updated_control.id_control,
        control_type_id=updated_control.control_type_id,
        description=updated_control.description,
        frequency=updated_control.frequency,
        responsible_id=updated_control.responsible_id
    )

@router.delete("/controls/{control_id}", response_model=dict)
async def delete_control_endpoint(control_id: int, db: AsyncSession = Depends(get_db)):
    repository = ControlRepository(db)
    await delete_control(control_id, repository)
    return {"detail": "Control deleted"}