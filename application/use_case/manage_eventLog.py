from domain.entities.Event_Log import EventLog, EventLogDesc
from domain.repositories.eventLog_repository import EventLogRepository

async def create_event_log(event_log_data: EventLog, repository: EventLogRepository) -> EventLog:
    return await repository.create_event_log(event_log_data)

async def get_event_log(event_log_id: int, repository: EventLogRepository) -> EventLog:
    return await repository.get_event_log(event_log_id)

async def get_all_event_logs(repository: EventLogRepository) -> list[EventLog]:
    return await repository.get_all_event_logs()

async def get_description_eventlog(repository: EventLogRepository) -> list[EventLogDesc]:
    print("entre al manager de eventlog description")
    return await repository.get_desc_event_logs()
    
async def update_event_log(event_log_id: int, event_log_data: EventLog, repository: EventLogRepository) -> EventLog:
    return await repository.update_event_log(event_log_id, event_log_data)

async def delete_event_log(event_log_id: int, repository: EventLogRepository) -> None:
    await repository.delete_event_log(event_log_id)