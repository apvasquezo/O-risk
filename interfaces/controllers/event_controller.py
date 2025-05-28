from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.event_repository import EventRepository
from application.use_case.manage_event import (
    create_event,
    get_event,
    get_all_events,
    update_event,
    delete_event,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/events",
    tags=["Eventos"],
    dependencies=[Depends(role_required("admin"))] 
)

class EventCreate(BaseModel):
    risk_type_id: int
    factor: str
    description: str
    probability_id: int
    impact_id: int

class EventResponse(BaseModel):
    id_event: int
    risk_type_id: int
    factor: str
    description: str
    probability_id: int
    impact_id: int

@router.post("/", response_model=EventResponse, status_code=201)
async def create_event_endpoint(event: EventCreate, db: AsyncSession = Depends(get_async_session)):
    repository = EventRepository(db)
    created = await create_event(event, repository)
    return EventResponse(**created.model_dump())

@router.get("/{event_id}", response_model=EventResponse)
async def read_event_endpoint(event_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = EventRepository(db)
    event = await get_event(event_id, repository)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return EventResponse(**event.model_dump())

@router.get("/", response_model=List[EventResponse])
async def read_all_events_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = EventRepository(db)
    events = await get_all_events(repository)
    return [EventResponse(**e.model_dump()) for e in events]

@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(event_id: int, event: EventCreate, db: AsyncSession = Depends(get_async_session)):
    repository = EventRepository(db)
    updated = await update_event(event_id, event, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return EventResponse(**updated.model_dump())

@router.delete("/{event_id}", response_model=dict)
async def delete_event_endpoint(event_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = EventRepository(db)
    await delete_event(event_id, repository)
    return {"detail": "Evento eliminado"}
