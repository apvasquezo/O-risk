from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.process_repository import ProcessRepository
from application.use_case.manage_process import (
    create_process,
    get_process,
    get_all_processes,
    update_process,
    delete_process
)
from utils.auth import role_required

router = APIRouter(
    prefix="/processes",
    tags=["Procesos"],
    dependencies=[Depends(role_required("admin"))]
)

class ProcessCreate(BaseModel):
    macroprocess_id: int
    description: str
    personal_id: str

class ProcessResponse(BaseModel):
    id_process: int
    macroprocess_id: int
    description: str
    personal_id: str

@router.post("/", response_model=ProcessResponse, status_code=201)
async def create_process_endpoint(process: ProcessCreate, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    created = await create_process(process, repository)
    return ProcessResponse(**created.model_dump())

@router.get("/{process_id}", response_model=ProcessResponse)
async def get_process_id(process_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    process = await get_process(process_id, repository)
    if not process:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return ProcessResponse(**process.model_dump())

@router.get("/", response_model=List[ProcessResponse])
async def read_processes(db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    processes = await get_all_processes(repository)
    return [ProcessResponse(**p.model_dump()) for p in processes]

@router.put("/{process_id}", response_model=ProcessResponse)
async def update_process_endpoint(process_id: int, process: ProcessCreate, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    updated = await update_process(process_id, process, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return ProcessResponse(**updated.model_dump())

@router.delete("/{process_id}", response_model=dict)
async def delete_process_endpoint(process_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    await delete_process(process_id, repository)
    return {"detail": "Proceso eliminado"}
