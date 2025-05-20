from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.risk_factor_repository import RiskFactorRepository
from application.use_case.manage_riskfactor import (
    create_risk_factor,
    get_risk_factor,
    get_all_risk_factors,
    update_risk_factor,
    delete_risk_factor,
)

router = APIRouter()

class RiskFactorCreate(BaseModel):
    risk_type_id: int
    description: str

class RiskFactorResponse(BaseModel):
    id_factor: int
    risk_type_id: int
    description: str

@router.post("/risk-factors/", response_model=RiskFactorResponse)
async def create_risk_factor_endpoint(risk_factor: RiskFactorCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskFactorRepository(db)
    created_risk_factor = await create_risk_factor(risk_factor, repository)
    return RiskFactorResponse(
        id_factor=created_risk_factor.id_factor,
        risk_type_id=created_risk_factor.risk_type_id,
        description=created_risk_factor.description
    )

@router.get("/risk-factors/{risk_factor_id}", response_model=RiskFactorResponse)
async def read_risk_factor_endpoint(risk_factor_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskFactorRepository(db)
    risk_factor = await get_risk_factor(risk_factor_id, repository)
    if not risk_factor:
        raise HTTPException(status_code=404, detail="Risk Factor not found")
    return RiskFactorResponse(
        id_factor=risk_factor.id_factor,
        risk_type_id=risk_factor.risk_type_id,
        description=risk_factor.description
    )

@router.get("/risk-factors/", response_model=List[RiskFactorResponse])
async def read_all_risk_factors_endpoint(db: AsyncSession = Depends(get_db)):
    repository = RiskFactorRepository(db)
    risk_factors = await get_all_risk_factors(repository)
    return [
        RiskFactorResponse(
            id_factor=factor.id_factor, 
            risk_type_id=factor.risk_type_id, 
            description=factor.description
        ) for factor in risk_factors
    ]

@router.put("/risk-factors/{risk_factor_id}", response_model=RiskFactorResponse)
async def update_risk_factor_endpoint(risk_factor_id: int, risk_factor: RiskFactorCreate, db: AsyncSession = Depends(get_db)):
    repository = RiskFactorRepository(db)
    updated_risk_factor = await update_risk_factor(risk_factor_id, risk_factor, repository)
    if not updated_risk_factor:
        raise HTTPException(status_code=404, detail="Risk Factor not found")
    return RiskFactorResponse(
        id_factor=updated_risk_factor.id_factor,
        risk_type_id=updated_risk_factor.risk_type_id,
        description=updated_risk_factor.description
    )

@router.delete("/risk-factors/{risk_factor_id}", response_model=dict)
async def delete_risk_factor_endpoint(risk_factor_id: int, db: AsyncSession = Depends(get_db)):
    repository = RiskFactorRepository(db)
    await delete_risk_factor(risk_factor_id, repository)
    return {"detail": "Risk Factor deleted"}