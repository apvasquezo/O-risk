from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.risk_control_type_repository import RiskControlTypeRepository
from application.use_case.manage_riskcontroltype import (
    create_risk_control_type,
    get_risk_control_type,
    get_all_risk_control_types,
    update_risk_control_type,
    delete_risk_control_type,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/risk-control-types",
    tags=["Tipos de Control"],
    dependencies=[Depends(role_required("super"))]
)

class RiskControlTypeCreate(BaseModel):
    description: str

class RiskControlTypeResponse(BaseModel):
    id_controltype: int
    description: str

@router.post("/", response_model=RiskControlTypeResponse, status_code=201)
async def create_risk_control_type_endpoint(control_type: RiskControlTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    created = await create_risk_control_type(control_type, repository)
    return RiskControlTypeResponse(**created.model_dump())

@router.get("/{control_type_id}", response_model=RiskControlTypeResponse)
async def read_risk_control_type_endpoint(control_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    control_type = await get_risk_control_type(control_type_id, repository)
    if not control_type:
        raise HTTPException(status_code=404, detail="Tipo de control no encontrado")
    return RiskControlTypeResponse(**control_type.model_dump())

@router.get("/", response_model=List[RiskControlTypeResponse])
async def read_all_risk_control_types_endpoint(db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    control_types = await get_all_risk_control_types(repository)
    return [RiskControlTypeResponse(**ct.model_dump()) for ct in control_types]

@router.put("/{control_type_id}", response_model=RiskControlTypeResponse)
async def update_risk_control_type_endpoint(control_type_id: int, control_type: RiskControlTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    updated = await update_risk_control_type(control_type_id, control_type, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Tipo de control no encontrado")
    return RiskControlTypeResponse(**updated.model_dump())

@router.delete("/{control_type_id}", response_model=dict)
async def delete_risk_control_type_endpoint(control_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    await delete_risk_control_type(control_type_id, repository)
    return {"detail": "Tipo de control eliminado"}
