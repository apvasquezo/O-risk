from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.cause_repository import CauseRepository
from application.use_case.manage_cause import (
    create_cause,
    get_cause,
    get_all_cause,
    update_cause,
    delete_cause,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/causes",
    tags=["Causas"],
    dependencies=[Depends(role_required("admin"))]
)

class CauseCreate(BaseModel):
    description: str

class CauseResponse(BaseModel):
    id_cause: int
    description: str

@router.post("/", response_model=CauseResponse, status_code=201)
async def create_cause_endpoint(cause: CauseCreate, db: AsyncSession = Depends(get_db)):
    repository = CauseRepository(db)
    created = await create_cause(cause, repository)
    return CauseResponse(**created.model_dump())

@router.get("/{cause_id}", response_model=CauseResponse)
async def read_cause_endpoint(cause_id: int, db: AsyncSession = Depends(get_db)):
    repository = CauseRepository(db)
    cause = await get_cause(cause_id, repository)
    if not cause:
        raise HTTPException(status_code=404, detail="Causa no encontrada")
    return CauseResponse(**cause.model_dump())

@router.get("/", response_model=List[CauseResponse])
async def read_all_causes_endpoint(db: AsyncSession = Depends(get_db)):
    repository = CauseRepository(db)
    causes = await get_all_cause(repository)
    return [CauseResponse(**c.model_dump()) for c in causes]

@router.put("/{cause_id}", response_model=CauseResponse)
async def update_cause_endpoint(cause_id: int, cause: CauseCreate, db: AsyncSession = Depends(get_db)):
    repository = CauseRepository(db)
    updated = await update_cause(cause_id, cause, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Causa no encontrada")
    return CauseResponse(**updated.model_dump())

@router.delete("/{cause_id}", status_code=204)
async def delete_cause_endpoint(cause_id: int, db: AsyncSession = Depends(get_db)):
    repository = CauseRepository(db)
    await delete_cause(cause_id, repository)
    return {"detail": "Causa eliminada"}
