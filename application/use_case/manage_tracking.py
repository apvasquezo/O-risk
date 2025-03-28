from domain.entities.Tracking import Tracking
from domain.repositories.tracking_repository import TrackingRepository

async def create_tracking(tracking_data: Tracking, repository: TrackingRepository) -> Tracking:
    return await repository.create_tracking(tracking_data)

async def get_tracking(tracking_id: int, repository: TrackingRepository) -> Tracking:
    return await repository.get_tracking(tracking_id)

async def get_all_trackings(repository: TrackingRepository) -> list[Tracking]:
    return await repository.get_all_trackings()

async def update_tracking(tracking_id: int, tracking_data: Tracking, repository: TrackingRepository) -> Tracking:
    return await repository.update_tracking(tracking_id, tracking_data)

async def delete_tracking(tracking_id: int, repository: TrackingRepository) -> None:
    await repository.delete_tracking(tracking_id)