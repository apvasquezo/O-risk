from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Notification as ORMNotification
from domain.entities.Notification import Notification as NotificationEntity

class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notification(self, notification: NotificationEntity) -> NotificationEntity:
        stmt = insert(ORMNotification).values(
            message=notification.message,
            suggestion_control=notification.suggestion_control,
            date_send=notification.date_send,
            user_id=notification.user_id,
            eventlog_id=notification.eventlog_id
        ).returning(
            ORMNotification.id,
            ORMNotification.message,
            ORMNotification.suggestion_control,
            ORMNotification.date_send,
            ORMNotification.user_id,
            ORMNotification.eventlog_id
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row = result.fetchone()
            if row:
                return NotificationEntity(
                    id=row.id,
                    message=row.message,
                    suggestion_control=row.suggestion_control,
                    date_send=row.date_send,
                    user_id=row.user_id,
                    eventlog_id=row.eventlog_id
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Notification already exists") from e

    async def get_notification(self, notification_id: int) -> Optional[NotificationEntity]:
        stmt = select(ORMNotification).where(ORMNotification.id == notification_id)
        result = await self.session.execute(stmt)
        notification = result.scalar_one_or_none()
        if notification:
            return NotificationEntity(
                id=notification.id,
                message=notification.message,
                suggestion_control=notification.suggestion_control,
                date_send=notification.date_send,
                user_id=notification.user_id,
                eventlog_id=notification.eventlog_id
            )
        return None

    async def get_all_notifications(self) -> List[NotificationEntity]:
        stmt = select(ORMNotification)
        result = await self.session.execute(stmt)
        notifications = result.scalars().all()
        return [
            NotificationEntity(
                id=n.id,
                message=n.message,
                suggestion_control=n.suggestion_control,
                date_send=n.date_send,
                user_id=n.user_id,
                eventlog_id=n.eventlog_id
            ) for n in notifications
        ]

    async def update_notification(self, notification_id: int, notification: NotificationEntity) -> Optional[NotificationEntity]:
        stmt = update(ORMNotification).where(ORMNotification.id == notification_id).values(
            message=notification.message,
            suggestion_control=notification.suggestion_control,
            date_send=notification.date_send,
            user_id=notification.user_id,
            eventlog_id=notification.eventlog_id
        ).returning(
            ORMNotification.id,
            ORMNotification.message,
            ORMNotification.suggestion_control,
            ORMNotification.date_send,
            ORMNotification.user_id,
            ORMNotification.eventlog_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return NotificationEntity(
                id=row.id,
                message=row.message,
                suggestion_control=row.suggestion_control,
                date_send=row.date_send,
                user_id=row.user_id,
                eventlog_id=row.eventlog_id
            )
        return None

    async def delete_notification(self, notification_id: int) -> None:
        stmt = delete(ORMNotification).where(ORMNotification.id == notification_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount == 0:
            raise ValueError(f"Notification with id {notification_id} not found")