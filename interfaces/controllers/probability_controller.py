from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.probability_repository import ProbabilityRepository
from application.use_case.manage_probability import (
    create_probability,
    get_probability,
    get_all_probabilities,
    update_probability,
    delete_probability,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/probabilities",
    tags=["Probabilidades"],
    dependencies=[Depends(role_required("super"))]
)

class ProbabilityCreate(BaseModel):
    level: int
    description: str
    definition: str
    criteria_por: float

class ProbabilityResponse(BaseModel):
    level: int
    description: str
    definition: str
    criteria_por: float

@router.post("/", response_model=ProbabilityResponse, status_code=201)
async def create_probability_endpoint(probability: ProbabilityCreate, db: AsyncSession = Depends(get_async_session)):
    repository = ProbabilityRepository(db)
    created = await create_probability(probability, repository)
    return ProbabilityResponse(**created.model_dump())

@router.get("/{probability_id}", response_model=ProbabilityResponse)
async def read_probability_endpoint(probability_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = ProbabilityRepository(db)
    probability = await get_probability(probability_id, repository)
    if not probability:
        raise HTTPException(status_code=404, detail="Probabilidad no encontrada")
    return ProbabilityResponse(**probability.model_dump())

@router.get("/", response_model=List[ProbabilityResponse])
async def read_all_probabilities_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = ProbabilityRepository(db)
    probabilities = await get_all_probabilities(repository)
    return [ProbabilityResponse(**p.model_dump()) for p in probabilities]

@router.put("/{probability_id}", response_model=ProbabilityResponse)
async def update_probability_endpoint(probability_id: int, probability: ProbabilityCreate, db: AsyncSession = Depends(get_async_session)):
    repository = ProbabilityRepository(db)
    updated = await update_probability(probability_id, probability, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Probabilidad no encontrada")
    return ProbabilityResponse(**updated.model_dump())

@router.delete("/{probability_id}", response_model=dict)
async def delete_probability_endpoint(probability_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = ProbabilityRepository(db)
    await delete_probability(probability_id, repository)
    return {"detail": "Probabilidad eliminada"}
