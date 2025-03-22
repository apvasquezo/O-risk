from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.tracking_repository import TrackingRepository
from application.use_case.manage_tracking import (
    create_tracking,
    get_tracking,
    get_all_trackings,
    update_tracking,
    delete_tracking,
)

router = APIRouter()

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

@router.post("/tracking/", response_model=TrackingResponse)
async def create_tracking_endpoint(tracking: TrackingCreate, db: AsyncSession = Depends(get_db)):
    repository = TrackingRepository(db)
    created_tracking = await create_tracking(tracking, repository)
    return TrackingResponse(
        id=created_tracking.id,
        user_id=created_tracking.user_id,
        control_id=created_tracking.control_id,
        event_id=created_tracking.event_id,
        tracking_date=created_tracking.tracking_date
    )

@router.get("/tracking/{tracking_id}", response_model=TrackingResponse)
async def read_tracking_endpoint(tracking_id: int, db: AsyncSession = Depends(get_db)):
    repository = TrackingRepository(db)
    tracking = await get_tracking(tracking_id, repository)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking not found")
    return TrackingResponse(
        id=tracking.id,
        user_id=tracking.user_id,
        control_id=tracking.control_id,
        event_id=tracking.event_id,
        tracking_date=tracking.tracking_date
    )

@router.get("/tracking/", response_model=List[TrackingResponse])
async def read_all_trackings_endpoint(db: AsyncSession = Depends(get_db)):
    repository = TrackingRepository(db)
    trackings = await get_all_trackings(repository)
    return [
        TrackingResponse(
            id=t.id,
            user_id=t.user_id,
            control_id=t.control_id,
            event_id=t.event_id,
            tracking_date=t.tracking_date
        ) for t in trackings
    ]

@router.put("/tracking/{tracking_id}", response_model=TrackingResponse)
async def update_tracking_endpoint(tracking_id: int, tracking: TrackingCreate, db: AsyncSession = Depends(get_db)):
    repository = TrackingRepository(db)
    updated_tracking = await update_tracking(tracking_id, tracking, repository)
    if not updated_tracking:
        raise HTTPException(status_code=404, detail="Tracking not found")
    return TrackingResponse(
        id=updated_tracking.id,
        user_id=updated_tracking.user_id,
        control_id=updated_tracking.control_id,
        event_id=updated_tracking.event_id,
        tracking_date=updated_tracking.tracking_date
    )

@router.delete("/tracking/{tracking_id}", response_model=dict)
async def delete_tracking_endpoint(tracking_id: int, db: AsyncSession = Depends(get_db)):
    repository = TrackingRepository(db)
    await delete_tracking(tracking_id, repository)
    return {"detail": "Tracking deleted"}