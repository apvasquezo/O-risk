from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.impact_repository import ImpactRepository
from application.use_case.manage_impact import (
    create_impact,
    get_impact,
    get_all_impacts,
    update_impact,
    delete_impact,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/impacts",
    tags=["Impactos"],
    dependencies=[Depends(role_required("super"))]
)

class ImpactCreate(BaseModel):
    level: int
    description: str
    definition: str
    criteria_smlv: float

class ImpactResponse(BaseModel):
    level: int
    description: str
    definition: str
    criteria_smlv: float

@router.post("/", response_model=ImpactResponse, status_code=201)
async def create_impact_endpoint(impact: ImpactCreate, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    created = await create_impact(impact, repository)
    return ImpactResponse(**created.model_dump())

@router.get("/{impact_id}", response_model=ImpactResponse)
async def read_impact_endpoint(impact_id: int, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    impact = await get_impact(impact_id, repository)
    if not impact:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")
    return ImpactResponse(**impact.model_dump())

@router.get("/", response_model=List[ImpactResponse])
async def read_all_impacts_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    impacts = await get_all_impacts(repository)
    return [ImpactResponse(**i.model_dump()) for i in impacts]

@router.put("/{impact_id}", response_model=ImpactResponse)
async def update_impact_endpoint(impact_id: int, impact: ImpactCreate, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    updated = await update_impact(impact_id, impact, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")
    return ImpactResponse(**updated.model_dump())

@router.delete("/{impact_id}", response_model=dict)
async def delete_impact_endpoint(impact_id: int, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    await delete_impact(impact_id, repository)
    return {"detail": "Impacto eliminado"}
