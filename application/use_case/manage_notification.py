from domain.entities.Notification import Notification
from domain.repositories.notification_repository import NotificationRepository

async def create_notification(notification_data: Notification, repository: NotificationRepository) -> Notification:
    return await repository.create_notification(notification_data)

async def get_notification(notification_id: int, repository: NotificationRepository) -> Notification:
    return await repository.get_notification(notification_id)

async def get_all_notifications(repository: NotificationRepository) -> list[Notification]:
    return await repository.get_all_notifications()

async def update_notification(notification_id: int, notification_data: Notification, repository: NotificationRepository) -> Notification:
    return await repository.update_notification(notification_id, notification_data)

async def delete_notification(notification_id: int, repository: NotificationRepository) -> None:
    await repository.delete_notification(notification_id)