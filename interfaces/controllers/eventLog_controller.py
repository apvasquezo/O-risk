from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.eventLog_repository import EventLogRepository
from application.use_case.manage_eventLog import (
    create_event_log,
    get_event_log,
    get_all_event_logs,
    update_event_log,
    delete_event_log,
)

router = APIRouter()

class EventLogCreate(BaseModel):
    id: Optional[int]=None
    event_id: int
    description:str
    start_date: datetime 
    end_date: Optional[datetime] 
    discovery_date: Optional[datetime] 
    accounting_date: Optional[datetime]
    amount: Optional[float] 
    recovered_amount: Optional[float] 
    insurance_recovery: Optional[float] 
    risk_factor_id: int 
    product_id: int 
    process_id: int 
    channel_id: int 
    city: Optional[str] 
    responsible_id: int 
    status: Optional[str]
     # Configuración para permitir tipos arbitrarios
    model_config = ConfigDict(arbitrary_types_allowed=True)

class EventLogResponse(EventLogCreate):
    id: int

@router.post("/event_logs/", response_model=EventLogResponse)
async def create_event_log_endpoint(event_log: EventLogCreate, db: AsyncSession = Depends(get_db)):
    repository = EventLogRepository(db)
    created_event_log = await create_event_log(event_log, repository)
    return EventLogResponse(**created_event_log.model_dump())

@router.get("/event_logs/{event_log_id}", response_model=EventLogResponse)
async def read_event_log_endpoint(event_log_id: int, db: AsyncSession = Depends(get_db)):
    repository = EventLogRepository(db)
    event_log = await get_event_log(event_log_id, repository)
    if not event_log:
        raise HTTPException(status_code=404, detail="EventLog not found")
    return EventLogResponse(**event_log.model_dump())

@router.get("/event_logs/", response_model=List[EventLogResponse])
async def read_all_event_logs_endpoint(db: AsyncSession = Depends(get_db)):
    repository = EventLogRepository(db)
    event_logs = await get_all_event_logs(repository)
    return [EventLogResponse(**e.model_dump()) for e in event_logs]

@router.put("/event_logs/{event_log_id}", response_model=EventLogResponse)
async def update_event_log_endpoint(event_log_id: int, event_log: EventLogCreate, db: AsyncSession = Depends(get_db)):
    repository = EventLogRepository(db)
    updated_event_log = await update_event_log(event_log_id, event_log, repository)
    if not updated_event_log:
        raise HTTPException(status_code=404, detail="EventLog not found")
    return EventLogResponse(**updated_event_log.model_dump())

@router.delete("/event_logs/{event_log_id}", response_model=dict)
async def delete_event_log_endpoint(event_log_id: int, db: AsyncSession = Depends(get_db)):
    repository = EventLogRepository(db)
    await delete_event_log(event_log_id, repository)
    return {"detail": "EventLog deleted"}
