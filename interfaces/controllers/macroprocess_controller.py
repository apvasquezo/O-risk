from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.macroprocess_repository import MacroprocessRepository

router = APIRouter()

class MacroprocessCreate(BaseModel):
    description: str

class MacroprocessResponse(BaseModel):
    id_macro: int
    description: str

@router.post("/macroprocesses/", response_model=MacroprocessResponse)
async def create_macroprocess(macroprocess: MacroprocessCreate, db: AsyncSession = Depends(get_db)):
    repository = MacroprocessRepository(db)
    created_macroprocess = await repository.create_macroprocess(macroprocess)
    return MacroprocessResponse(id_macro=created_macroprocess.id_macro, description=created_macroprocess.description)

@router.get("/macroprocesses/{macroprocess_id}", response_model=MacroprocessResponse)
async def read_macroprocess(macroprocess_id: int, db: AsyncSession = Depends(get_db)):
    repository = MacroprocessRepository(db)
    macroprocess = await repository.get_macroprocess(macroprocess_id)
    if macroprocess is None:
        raise HTTPException(status_code=404, detail="Macroprocess not found")
    return MacroprocessResponse(id_macro=macroprocess.id_macro, description=macroprocess.description)

@router.get("/macroprocesses/", response_model=List[MacroprocessResponse])
async def read_macroprocesses(db: AsyncSession = Depends(get_db)):
    repository = MacroprocessRepository(db)
    macroprocesses = await repository.get_all_macroprocesses()
    return [MacroprocessResponse(id_macro=m.id_macro, description=m.description) for m in macroprocesses]

@router.put("/macroprocesses/{macroprocess_id}", response_model=MacroprocessResponse)
async def update_macroprocess(macroprocess_id: int, macroprocess: MacroprocessCreate, db: AsyncSession = Depends(get_db)):
    repository = MacroprocessRepository(db)
    updated_macroprocess = await repository.update_macroprocess(macroprocess_id, macroprocess)
    if updated_macroprocess is None:
        raise HTTPException(status_code=404, detail="Macroprocess not found")
    return MacroprocessResponse(id_macro=updated_macroprocess.id_macro, description=updated_macroprocess.description)

@router.delete("/macroprocesses/{macroprocess_id}", response_model=dict)
async def delete_macroprocess(macroprocess_id: int, db: AsyncSession = Depends(get_db)):
    repository = MacroprocessRepository(db)
    await repository.delete_macroprocess(macroprocess_id)
    return {"detail": "Macroprocess deleted"}