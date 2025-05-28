from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.risk_type_repository import RiskTypeRepository
from application.use_case.manage_risktype import (
    create_risk_type,
    get_risk_type,
    get_all_risk_types,
    update_risk_type,
    delete_risk_type,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/risk-types",
    tags=["Tipos de Riesgo"],
    dependencies=[Depends(role_required("super"))]
)

class RiskTypeCreate(BaseModel):
    category_id: int
    description: str

class RiskTypeResponse(BaseModel):
    id_risktype: int
    category_id: int
    description: str

@router.post("/", response_model=RiskTypeResponse, status_code=201)
async def create_risk_type_endpoint(risk_type: RiskTypeCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskTypeRepository(db)
    created = await create_risk_type(risk_type, repository)
    return RiskTypeResponse(**created.model_dump())

@router.get("/{risk_type_id}", response_model=RiskTypeResponse)
async def read_risk_type_endpoint(risk_type_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskTypeRepository(db)
    risk_type = await get_risk_type(risk_type_id, repository)
    if not risk_type:
        raise HTTPException(status_code=404, detail="Tipo de riesgo no encontrado")
    return RiskTypeResponse(**risk_type.model_dump())

@router.get("/", response_model=List[RiskTypeResponse])
async def read_all_risk_types_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = RiskTypeRepository(db)
    risk_types = await get_all_risk_types(repository)
    return [RiskTypeResponse(**r.model_dump()) for r in risk_types]

@router.put("/{risk_type_id}", response_model=RiskTypeResponse)
async def update_risk_type_endpoint(risk_type_id: int, risk_type: RiskTypeCreate, db: AsyncSession = Depends(get_async_session)):
    repository = RiskTypeRepository(db)
    updated = await update_risk_type(risk_type_id, risk_type, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Tipo de riesgo no encontrado")
    return RiskTypeResponse(**updated.model_dump())

@router.delete("/{risk_type_id}", response_model=dict)
async def delete_risk_type_endpoint(risk_type_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = RiskTypeRepository(db)
    await delete_risk_type(risk_type_id, repository)
    return {"detail": "Tipo de riesgo eliminado"}
