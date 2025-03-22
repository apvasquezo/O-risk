from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel, ConfigDict
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

router = APIRouter()

class NotificationCreate(BaseModel):
    message: str
    suggestion_control: str
    date_send: datetime
    user_id: int
    eventlog_id: int
     # Configuración para permitir tipos arbitrarios
    model_config = ConfigDict(arbitrary_types_allowed=True)

class NotificationResponse(BaseModel):
    id: int
    message: str
    suggestion_control: str
    date_send: datetime
    user_id: int
    eventlog_id: int

@router.post("/notifications/", response_model=NotificationResponse)
async def create_notification_endpoint(notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    created_notification = await create_notification(notification, repository)
    return NotificationResponse(**created_notification.model_dump())

@router.get("/notifications/{notification_id}", response_model=NotificationResponse)
async def read_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    notification = await get_notification(notification_id, repository)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse(**notification.model_dump())

@router.get("/notifications/", response_model=List[NotificationResponse])
async def read_all_notifications_endpoint(db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    notifications = await get_all_notifications(repository)
    return [NotificationResponse(**n.model_dump()) for n in notifications]

@router.put("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification_endpoint(notification_id: int, notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    updated_notification = await update_notification(notification_id, notification, repository)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse(**updated_notification.model_dump())

@router.delete("/notifications/{notification_id}", response_model=dict)
async def delete_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    repository = NotificationRepository(db)
    await delete_notification(notification_id, repository)
    return {"detail": "Notification deleted"}