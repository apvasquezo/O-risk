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
from utils.auth import role_required

router = APIRouter(
    prefix="/consequences",
    tags=["Consecuencias"],
    dependencies=[Depends(role_required("admin"))] 
)

class ConsequenceCreate(BaseModel):
    description: str

class ConsequenceResponse(BaseModel):
    id_consequence: int
    description: str

@router.post("/", response_model=ConsequenceResponse, status_code=201)
async def create_consequence_endpoint(consequence: ConsequenceCreate, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    created = await create_consequence(consequence, repository)
    return ConsequenceResponse(**created.model_dump())

@router.get("/{consequence_id}", response_model=ConsequenceResponse)
async def read_consequence_endpoint(consequence_id: int, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    consequence = await get_consequence(consequence_id, repository)
    if not consequence:
        raise HTTPException(status_code=404, detail="Consecuencia no encontrada")
    return ConsequenceResponse(**consequence.model_dump())

@router.get("/", response_model=List[ConsequenceResponse])
async def read_all_consequence_endpoint(db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    consequences = await get_all_consequence(repository)
    return [ConsequenceResponse(**c.model_dump()) for c in consequences]

@router.put("/{consequence_id}", response_model=ConsequenceResponse)
async def update_consequence_endpoint(consequence_id: int, consequence: ConsequenceCreate, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    updated = await update_consequence(consequence_id, consequence, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Consecuencia no encontrada")
    return ConsequenceResponse(**updated.model_dump())

@router.delete("/{consequence_id}", status_code=204)
async def delete_consequence_endpoint(consequence_id: int, db: AsyncSession = Depends(get_db)):
    repository = ConsequenceRepository(db)
    await delete_consequence(consequence_id, repository)
    return {"detail": "Consecuencia eliminada"}
