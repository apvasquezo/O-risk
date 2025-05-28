from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.tracking_repository import TrackingRepository
from application.use_case.manage_tracking import (
    create_tracking,
    get_tracking,
    get_all_trackings,
    update_tracking,
    delete_tracking,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/trackings",
    tags=["Seguimiento de Controles"],
    dependencies=[Depends(role_required("admin"))]
)

class TrackingCreate(BaseModel):
    user_id: int
    control_id: int
    event_id: int
    tracking_date: datetime

class TrackingResponse(BaseModel):
    id: int
    user_id: int
    control_id: int
    event_id: int
    tracking_date: datetime

@router.post("/", response_model=TrackingResponse, status_code=201)
async def create_tracking_endpoint(tracking: TrackingCreate, db: AsyncSession = Depends(get_async_session)):
    repository = TrackingRepository(db)
    created = await create_tracking(tracking, repository)
    return TrackingResponse(**created.model_dump())

@router.get("/{tracking_id}", response_model=TrackingResponse)
async def read_tracking_endpoint(tracking_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = TrackingRepository(db)
    tracking = await get_tracking(tracking_id, repository)
    if not tracking:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return TrackingResponse(**tracking.model_dump())

@router.get("/", response_model=List[TrackingResponse])
async def read_all_trackings_endpoint(db: AsyncSession = Depends(get_async_session)):
    repository = TrackingRepository(db)
    trackings = await get_all_trackings(repository)
    return [TrackingResponse(**t.model_dump()) for t in trackings]

@router.put("/{tracking_id}", response_model=TrackingResponse)
async def update_tracking_endpoint(tracking_id: int, tracking: TrackingCreate, db: AsyncSession = Depends(get_async_session)):
    repository = TrackingRepository(db)
    updated = await update_tracking(tracking_id, tracking, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return TrackingResponse(**updated.model_dump())

@router.delete("/{tracking_id}", response_model=dict)
async def delete_tracking_endpoint(tracking_id: int, db: AsyncSession = Depends(get_async_session)):
    repository = TrackingRepository(db)
    await delete_tracking(tracking_id, repository)
    return {"detail": "Seguimiento eliminado"}
