from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.event_repository import EventRepository
from application.use_case.manage_event import (
    create_event,
    get_event,
    get_all_events,
    update_event,
    delete_event,
)

router = APIRouter()

class EventCreate(BaseModel):
    risk_type_id: int
    factor: str
    description: str
    probability_id: int
    impact_id: int

class EventResponse(BaseModel):
    id: int
    risk_type_id: int
    factor: str
    description: str
    probability_id: int
    impact_id: int

@router.post("/events/", response_model=EventResponse)
async def create_event_endpoint(event: EventCreate, db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    created_event = await create_event(event, repository)
    return EventResponse(**created_event.model_dump())  

@router.get("/events/{event_id}", response_model=EventResponse)
async def read_event_endpoint(event_id: int, db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    event = await get_event(event_id, repository)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(**event.model_dump())  

@router.get("/events/", response_model=List[EventResponse])
async def read_all_events_endpoint(db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    events = await get_all_events(repository)
    return [EventResponse(**e.model_dump()) for e in events]  

@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event_endpoint(event_id: int, event: EventCreate, db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    updated_event = await update_event(event_id, event, repository)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(**updated_event.model_dump())  

@router.delete("/events/{event_id}", response_model=dict)
async def delete_event_endpoint(event_id: int, db: AsyncSession = Depends(get_db)):
    repository = EventRepository(db)
    await delete_event(event_id, repository)
    return {"detail": "Event deleted"}