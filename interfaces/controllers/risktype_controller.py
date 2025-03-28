from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.risk_type_repository import RiskTypeRepository
from application.use_case.manage_risktype import (
    create_risk_type,
    get_risk_type,
    get_all_risk_types,
    update_risk_type,
    delete_risk_type,
)

router = APIRouter()

class RiskTypeCreate(BaseModel):
    category_id: int
    description: str

class RiskTypeResponse(BaseModel):
    id: int
    category_id: int
    description: str

@router.post("/risk-types/", response_model=RiskTypeResponse)
async def create_risk_type_endpoint(risk_type: RiskTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskTypeRepository(db)
    created_risk_type = await create_risk_type(risk_type, repository)
    return RiskTypeResponse(
        id=created_risk_type.id,
        category_id=created_risk_type.category_id,
        description=created_risk_type.description
    )

@router.get("/risk-types/{risk_type_id}", response_model=RiskTypeResponse)
async def read_risk_type_endpoint(risk_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskTypeRepository(db)
    risk_type = await get_risk_type(risk_type_id, repository)
    if not risk_type:
        raise HTTPException(status_code=404, detail="Risk Type not found")
    return RiskTypeResponse(
        id=risk_type.id,
        category_id=risk_type.category_id,
        description=risk_type.description
    )

@router.get("/risk-types/", response_model=List[RiskTypeResponse])
async def read_all_risk_types_endpoint(db: AsyncSession = Depends(get_db)):
    repository = RiskTypeRepository(db)
    risk_types = await get_all_risk_types(repository)
    return [
        RiskTypeResponse(id=risk.id, category_id=risk.category_id, description=risk.description)
        for risk in risk_types
    ]

@router.put("/risk-types/{risk_type_id}", response_model=RiskTypeResponse)
async def update_risk_type_endpoint(risk_type_id: int, risk_type: RiskTypeCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskTypeRepository(db)
    updated_risk_type = await update_risk_type(risk_type_id, risk_type, repository)
    if not updated_risk_type:
        raise HTTPException(status_code=404, detail="Risk Type not found")
    return RiskTypeResponse(
        id=updated_risk_type.id,
        category_id=updated_risk_type.category_id,
        description=updated_risk_type.description
    )

@router.delete("/risk-types/{risk_type_id}", response_model=dict)
async def delete_risk_type_endpoint(risk_type_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskTypeRepository(db)
    await delete_risk_type(risk_type_id, repository)
    return {"detail": "Risk Type deleted"}