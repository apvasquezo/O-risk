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

router = APIRouter()

class ImpactCreate(BaseModel):
    level: int
    description: str
    definition: str
    criteria_smlv: int

class ImpactResponse(BaseModel):
    id: int
    level: int
    description: str
    definition: str
    criteria_smlv: int

@router.post("/impacts/", response_model=ImpactResponse)
async def create_impact_endpoint(impact: ImpactCreate, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    created_impact = await create_impact(impact, repository)
    return ImpactResponse(**created_impact.model_dump())

@router.get("/impacts/{impact_id}", response_model=ImpactResponse)
async def read_impact_endpoint(impact_id: int, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    impact = await get_impact(impact_id, repository)
    if not impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    return ImpactResponse(**impact.model_dump())

@router.get("/impacts/", response_model=List[ImpactResponse])
async def read_all_impacts_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    impacts = await get_all_impacts(repository)
    return [ImpactResponse(**i.model_dump()) for i in impacts]

@router.put("/impacts/{impact_id}", response_model=ImpactResponse)
async def update_impact_endpoint(impact_id: int, impact: ImpactCreate, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    updated_impact = await update_impact(impact_id, impact, repository)
    if not updated_impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    return ImpactResponse(**updated_impact.model_dump())

@router.delete("/impacts/{impact_id}", response_model=dict)
async def delete_impact_endpoint(impact_id: int, db: AsyncSession = Depends(get_db)):
    repository = ImpactRepository(db)
    await delete_impact(impact_id, repository)
    return {"detail": "Impact deleted"}