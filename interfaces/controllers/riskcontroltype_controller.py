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

router = APIRouter()

class RiskControlTypeCreate(BaseModel):
    description: str

class RiskControlTypeResponse(BaseModel):
    id: int
    description: str

@router.post("/risk-control-types/", response_model=RiskControlTypeResponse)
async def create_risk_control_type_endpoint(control_type: RiskControlTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    created_control_type = await create_risk_control_type(control_type, repository)
    return RiskControlTypeResponse(id=created_control_type.id, description=created_control_type.description)

@router.get("/risk-control-types/{control_type_id}", response_model=RiskControlTypeResponse)
async def read_risk_control_type_endpoint(control_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    control_type = await get_risk_control_type(control_type_id, repository)
    if not control_type:
        raise HTTPException(status_code=404, detail="Risk Control Type not found")
    return RiskControlTypeResponse(id=control_type.id, description=control_type.description)

@router.get("/risk-control-types/", response_model=List[RiskControlTypeResponse])
async def read_all_risk_control_types_endpoint(db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    control_types = await get_all_risk_control_types(repository)
    return [RiskControlTypeResponse(id=ct.id, description=ct.description) for ct in control_types]

@router.put("/risk-control-types/{control_type_id}", response_model=RiskControlTypeResponse)
async def update_risk_control_type_endpoint(control_type_id: int, control_type: RiskControlTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    updated_control_type = await update_risk_control_type(control_type_id, control_type, repository)
    if not updated_control_type:
        raise HTTPException(status_code=404, detail="Risk Control Type not found")
    return RiskControlTypeResponse(id=updated_control_type.id, description=updated_control_type.description)

@router.delete("/risk-control-types/{control_type_id}", response_model=dict)
async def delete_risk_control_type_endpoint(control_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskControlTypeRepository(db)
    await delete_risk_control_type(control_type_id, repository)
    return {"detail": "Risk Control Type deleted"}