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

router = APIRouter()

class ProcessCreate(BaseModel):
    macroprocess_id: int
    description: str

class ProcessResponse(BaseModel):
    id: int
    macroprocess_id: int
    description: str

@router.post("/processes/", response_model=ProcessResponse)
async def create_process(process: ProcessCreate, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    created_process = await repository.create_process(process)
    return ProcessResponse(id=created_process.id, macroprocess_id=created_process.macroprocess_id, description=created_process.description)

@router.get("/processes/{process_id}", response_model=ProcessResponse)
async def get_process_id(process_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    process = await repository.get_process(process_id)
    if process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return ProcessResponse(id=process.id, macroprocess_id=process.macroprocess_id, description=process.description)

@router.get("/processes/", response_model=List[ProcessResponse])
async def read_processes(db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    processes = await repository.get_all_processes()
    return [ProcessResponse(id=p.id, macroprocess_id=p.macroprocess_id, description=p.description) for p in processes]

@router.put("/processes/{process_id}", response_model=ProcessResponse)
async def update_process(process_id: int, process: ProcessCreate, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    updated_process = await repository.update_process(process_id, process)
    if updated_process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return ProcessResponse(id=updated_process.id, macroprocess_id=updated_process.macroprocess_id, description=updated_process.description)

@router.delete("/processes/{process_id}", response_model=dict)
async def delete_process(process_id: int, db: AsyncSession = Depends(get_db)):
    repository = ProcessRepository(db)
    await repository.delete_process(process_id)
    return {"detail": "Process deleted"}