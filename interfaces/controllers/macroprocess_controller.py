from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.macroprocess_repository import MacroprocessRepository
from utils.auth import role_required

router = APIRouter(
    prefix="/macroprocesses",
    tags=["Macroprocesos"],
    #dependencies=[Depends(role_required("super"))]
)

class MacroprocessCreate(BaseModel):
    description: str

class MacroprocessResponse(BaseModel):
    id_macro: int
    description: str

@router.post("/", response_model=MacroprocessResponse, status_code=201)
async def create_macroprocess(macroprocess: MacroprocessCreate, db: AsyncSession = Depends(get_async_session), _: None = Depends(role_required("super"))):
    repository = MacroprocessRepository(db)
    created = await repository.create_macroprocess(macroprocess)
    return MacroprocessResponse(**created.model_dump())

@router.get("/{macroprocess_id}", response_model=MacroprocessResponse)
async def read_macroprocess(macroprocess_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = MacroprocessRepository(db)
    macroprocess = await repository.get_macroprocess(macroprocess_id)
    if macroprocess is None:
        raise HTTPException(status_code=404, detail="Macroproceso no encontrado")
    return MacroprocessResponse(**macroprocess.model_dump())

@router.get("/", response_model=List[MacroprocessResponse])
async def read_macroprocesses(db: AsyncSession = Depends(get_async_session)):
    repository = MacroprocessRepository(db)
    macroprocesses = await repository.get_all_macroprocesses()
    return [MacroprocessResponse(**m.model_dump()) for m in macroprocesses]

@router.put("/{macroprocess_id}", response_model=MacroprocessResponse)
async def update_macroprocess(macroprocess_id: int, macroprocess: MacroprocessCreate, db: AsyncSession = Depends(get_async_session)):
    repository = MacroprocessRepository(db)
    updated = await repository.update_macroprocess(macroprocess_id, macroprocess)
    if updated is None:
        raise HTTPException(status_code=404, detail="Macroproceso no encontrado")
    return MacroprocessResponse(**updated.model_dump())

@router.delete("/{macroprocess_id}", response_model=dict)
async def delete_macroprocess(macroprocess_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = MacroprocessRepository(db)
    await repository.delete_macroprocess(macroprocess_id)
    return {"detail": "Macroproceso eliminado"}
