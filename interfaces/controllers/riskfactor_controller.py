from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.risk_factor_repository import RiskFactorRepository
from application.use_case.manage_riskfactor import (
    create_risk_factor,
    get_risk_factor,
    get_all_risk_factors,
    update_risk_factor,
    delete_risk_factor,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/risk-factors",
    tags=["Factores de Riesgo"],
    dependencies=[Depends(role_required("super"))]
)

class RiskFactorCreate(BaseModel):
    risk_type_id: int
    description: str

class RiskFactorResponse(BaseModel):
    id_factor: int
    risk_type_id: int
    description: str

@router.post("/", response_model=RiskFactorResponse, status_code=201)
async def create_risk_factor_endpoint(risk_factor: RiskFactorCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskFactorRepository(db)
    created = await create_risk_factor(risk_factor, repository)
    return RiskFactorResponse(**created.model_dump())

@router.get("/{risk_factor_id}", response_model=RiskFactorResponse)
async def read_risk_factor_endpoint(risk_factor_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskFactorRepository(db)
    factor = await get_risk_factor(risk_factor_id, repository)
    if not factor:
        raise HTTPException(status_code=404, detail="Factor de riesgo no encontrado")
    return RiskFactorResponse(**factor.model_dump())

@router.get("/", response_model=List[RiskFactorResponse])
async def read_all_risk_factors_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = RiskFactorRepository(db)
    factors = await get_all_risk_factors(repository)
    return [RiskFactorResponse(**f.model_dump()) for f in factors]

@router.put("/{risk_factor_id}", response_model=RiskFactorResponse)
async def update_risk_factor_endpoint(risk_factor_id: int, risk_factor: RiskFactorCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskFactorRepository(db)
    updated = await update_risk_factor(risk_factor_id, risk_factor, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Factor de riesgo no encontrado")
    return RiskFactorResponse(**updated.model_dump())

@router.delete("/{risk_factor_id}", response_model=dict)
async def delete_risk_factor_endpoint(risk_factor_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskFactorRepository(db)
    await delete_risk_factor(risk_factor_id, repository)
    return {"detail": "Factor de riesgo eliminado"}
