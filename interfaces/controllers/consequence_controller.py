from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.consequence_repository import ConsequenceRepository
from application.use_case.manage_consequence import (
    create_consequence,
    get_consequence,
    get_all_consequence,
    update_consequence,
    delete_consequence,
)

router = APIRouter()

class ConsequenceCreate(BaseModel):
    description: str
    risk_factor_id: int
    event_id: int

class ConsequenceResponse(BaseModel):
    id_consequence: int
    description: str
    risk_factor_id: int
    event_id: int

@router.post("/consequence/", response_model=ConsequenceResponse, status_code=201)
async def create_consequence_endpoint(consequence: ConsequenceCreate, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    created_consequence = await create_consequence(consequence, repository)
    return ConsequenceResponse(
        id_consequence=created_consequence.id_consequence,
        description=created_consequence.description,
        risk_factor_id=created_consequence.risk_factor_id,
        event_id=created_consequence.event_id,
    )

@router.get("/consequence/{consequence_id}", response_model=ConsequenceResponse)
async def read_consequence_endpoint(consequence_id: int, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    consequence = await get_consequence(consequence_id, repository)
    if not consequence:
        raise HTTPException(status_code=404, detail="Consequence not found")
    return ConsequenceResponse(
        id_consequence=consequence.id_consequence,
        description=consequence.description,
        risk_factor_id=consequence.risk_factor_id,
        event_id=consequence.event_id,
    )

@router.get("/consequence/", response_model=List[ConsequenceResponse])
async def read_all_consequence_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    consequences = await get_all_consequence(repository)
    return [
        ConsequenceResponse(
            id_consequence=c.id,
            description=c.description,
            risk_factor_id=c.risk_factor_id,
            event_id=c.event_id,
        )
        for c in consequences
    ]

@router.put("/consequence/{consequence_id}", response_model=ConsequenceResponse)
async def update_consequence_endpoint(consequence_id: int, consequence: ConsequenceCreate, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    updated_consequence = await update_consequence(consequence_id, consequence, repository)
    if not updated_consequence:
        raise HTTPException(status_code=404, detail="Cause not found")
    return ConsequenceResponse(
        id_consequence=updated_consequence.id,
        description=updated_consequence.description,
        risk_factor_id=updated_consequence.risk_factor_id,
        event_id=updated_consequence.event_id,
    )

@router.delete("/consequence/{cconsequence_id}", status_code=204)
async def delete_concequence_endpoint(consequence_id: int, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    await delete_consequence(consequence_id, repository)
    return {"detail": "Consequence deleted"}