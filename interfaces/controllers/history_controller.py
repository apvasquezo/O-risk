from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.history_repository import HistoryRepository
from application.use_case.manage_history import (
    create_history,
    get_history,
    get_all_histories,
    update_history,
    delete_history,
)

router = APIRouter()

class HistoryCreate(BaseModel):
    eventlog_id: int
    control_id: int
    start_date: datetime
    end_date: Optional[datetime]
    value_risk: float
    model_config = ConfigDict(arbitrary_types_allowed=True)

class HistoryResponse(BaseModel):
    id: int
    eventlog_id: int
    control_id: int
    start_date: datetime
    end_date: Optional[datetime]
    value_risk: float

@router.post("/histories/", response_model=HistoryResponse)
async def create_history_endpoint(history: HistoryCreate, db: AsyncSession = Depends(get_db)):
    repository = HistoryRepository(db)
    created_history = await create_history(history, repository)
    return HistoryResponse(**created_history.model_dump())

@router.get("/histories/{history_id}", response_model=HistoryResponse)
async def read_history_endpoint(history_id: int, db: AsyncSession = Depends(get_db)):
    repository = HistoryRepository(db)
    history = await get_history(history_id, repository)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return HistoryResponse(**history.model_dump())

@router.get("/histories/", response_model=List[HistoryResponse])
async def read_all_histories_endpoint(db: AsyncSession = Depends(get_db)):
    repository = HistoryRepository(db)
    histories = await get_all_histories(repository)
    return [HistoryResponse(**h.model_dump()) for h in histories]

@router.put("/histories/{history_id}", response_model=HistoryResponse)
async def update_history_endpoint(history_id: int, history: HistoryCreate, db: AsyncSession = Depends(get_db)):
    repository = HistoryRepository(db)
    updated_history = await update_history(history_id, history, repository)
    if not updated_history:
        raise HTTPException(status_code=404, detail="History not found")
    return HistoryResponse(**updated_history.model_dump())

@router.delete("/histories/{history_id}", response_model=dict)
async def delete_history_endpoint(history_id: int, db: AsyncSession = Depends(get_db)):
    repository = HistoryRepository(db)
    await delete_history(history_id, repository)
    return {"detail": "History deleted"}