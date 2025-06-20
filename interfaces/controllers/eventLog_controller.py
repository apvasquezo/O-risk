from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.eventLog_repository import EventLogRepository
from application.use_case.manage_eventLog import (
    create_event_log,
    get_event_log,
    get_all_event_logs,
    get_description_eventlog,
    update_event_log,
    delete_event_log,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/event_logs",
    tags=["Registro de Riesgos"],
    dependencies=[Depends(role_required("admin"))]
)

class EventLogCreate(BaseModel):
    event_id: int
    description: str
    start_date: date
    end_date: Optional[date]
    discovery_date: Optional[date]
    accounting_date: Optional[date]
    amount: Optional[float]
    recovered_amount: Optional[float]
    insurance_recovery: Optional[float]
    acount: Optional[float]
    product_id: int
    process_id: int
    channel_id: int
    city: Optional[str]
    responsible_id: str
    status: Optional[str]
    cause1_id: int
    cause2_id: Optional[int]
    conse1_id: int
    conse2_id: Optional[int]

class EventLogResponse(BaseModel):
    id_eventlog: int
    event_id: int
    description: str
    start_date: date
    end_date: Optional[date]
    discovery_date: Optional[date]
    accounting_date: Optional[date]
    amount: Optional[float]
    recovered_amount: Optional[float]
    insurance_recovery: Optional[float]
    acount: Optional[float]
    product_id: int
    process_id: int
    channel_id: int
    city: Optional[str]
    responsible_id: str
    status: Optional[str]
    cause1_id: int
    cause2_id: Optional[int]
    conse1_id: int
    conse2_id: Optional[int]
    
class EventDescription (BaseModel):
    id_eventlog: int
    description: str
    

@router.post("/", response_model=EventLogResponse, status_code=201)
async def create_event_log_endpoint(event_log: EventLogCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EventLogRepository(db)
        created = await create_event_log(event_log, repository)
        return EventLogResponse(**created.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en create_event_log_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/name", response_model=List[EventDescription])
async def get_description_event(db: AsyncSession = Depends(get_async_session)):
    print("estoy en controller event log ")    
    try:
        repository= EventLogRepository(db)
        event_des= await get_description_eventlog(repository)
        return [EventDescription(id_eventlog=e.id_eventlog, description=e.description) for e in event_des]
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en get_description_event: {str(e)}")

@router.get("/{event_log_id}", response_model=EventLogResponse)
async def read_event_log_endpoint(event_log_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EventLogRepository(db)
        event_log = await get_event_log(event_log_id, repository)
        if not event_log:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return EventLogResponse(**event_log.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_event_log_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=List[EventLogResponse])
async def read_all_event_logs_endpoint(db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EventLogRepository(db)
        event_logs = await get_all_event_logs(repository)
        return [EventLogResponse(**e.model_dump()) for e in event_logs]
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_all_event_log_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/{event_log_id}", response_model=EventLogResponse)
async def update_event_log_endpoint(event_log_id: int, event_log: EventLogCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EventLogRepository(db)
        updated = await update_event_log(event_log_id, event_log, repository)
        if not updated:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return EventLogResponse(**updated.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en update_event_log_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{event_log_id}", response_model=dict)
async def delete_event_log_endpoint(event_log_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EventLogRepository(db)
        await delete_event_log(event_log_id, repository)
        return {"detail": "Registro eliminado"}
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en delete_event_log_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")