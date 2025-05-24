from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.notification_repository import NotificationRepository
from application.use_case.manage_notification import (
    create_notification,
    get_notification,
    get_all_notifications,
    update_notification,
    delete_notification,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/notifications",
    tags=["Notificaciones"],
    dependencies=[Depends(role_required("admin"))]
)

class NotificationCreate(BaseModel):
    message: str
    suggestion_control: str
    date_send: datetime
    user_id: int
    eventlog_id: int

class NotificationResponse(BaseModel):
    id: int
    message: str
    suggestion_control: str
    date_send: datetime
    user_id: int
    eventlog_id: int

@router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification_endpoint(notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    created = await create_notification(notification, repository)
    return NotificationResponse(**created.model_dump())

@router.get("/{notification_id}", response_model=NotificationResponse)
async def read_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    notification = await get_notification(notification_id, repository)
    if not notification:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return NotificationResponse(**notification.model_dump())

@router.get("/", response_model=List[NotificationResponse])
async def read_all_notifications_endpoint(db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    notifications = await get_all_notifications(repository)
    return [NotificationResponse(**n.model_dump()) for n in notifications]

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification_endpoint(notification_id: int, notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    updated = await update_notification(notification_id, notification, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return NotificationResponse(**updated.model_dump())

@router.delete("/{notification_id}", response_model=dict)
async def delete_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    await delete_notification(notification_id, repository)
    return {"detail": "Notificación eliminada"}
