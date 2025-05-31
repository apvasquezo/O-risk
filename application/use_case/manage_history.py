from domain.entities.History import History
from domain.repositories.history_repository import HistoryRepository

async def create_history(history_data: History, repository: HistoryRepository) -> History:
    return await repository.create_history(history_data)

async def get_history(history_id: int, repository: HistoryRepository) -> History:
    return await repository.get_history(history_id)

async def get_all_histories(repository: HistoryRepository) -> list[History]:
    return await repository.get_all_histories()

async def update_history(history_id: int, history_data: History, repository: HistoryRepository) -> History:
    return await repository.update_history(history_id, history_data)

async def delete_history(history_id: int, repository: HistoryRepository) -> None:
    await repository.delete_history(history_id)