from domain.entities.Process import Process
from domain.repositories.process_repository import ProcessRepository

async def create_process(macroprocess_id: int, description: str, repository: ProcessRepository) -> Process:
    process = Process(macroprocess_id=macroprocess_id, description=description)
    return await repository.create_process(process)

async def get_process(process_id: int, repository: ProcessRepository) -> Process:
    return await repository.get_process(process_id)

async def get_all_processes(repository: ProcessRepository) -> list[Process]:
    return await repository.get_all_processes()

async def update_process(process_id: int, macroprocess_id: int, description: str, repository: ProcessRepository) -> Process:
    process = Process(id=process_id, macroprocess_id=macroprocess_id, description=description)
    return await repository.update_process(process_id, process)

async def delete_process(process_id: int, repository: ProcessRepository) -> None:
    await repository.delete_process(process_id)