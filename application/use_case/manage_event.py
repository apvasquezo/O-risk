from domain.entities.Event import Event
from domain.repositories.event_repository import EventRepository

async def create_event(event_data: Event, repository: EventRepository) -> Event:
    return await repository.create_event(event_data)

async def get_event(event_id: int, repository: EventRepository) -> Event:
    return await repository.get_event(event_id)

async def get_all_events(repository: EventRepository) -> list[Event]:
    return await repository.get_all_events()

async def update_event(event_id: int, event_data: Event, repository: EventRepository) -> Event:
    return await repository.update_event(event_id, event_data)

async def delete_event(event_id: int, repository: EventRepository) -> None:
    await repository.delete_event(event_id)