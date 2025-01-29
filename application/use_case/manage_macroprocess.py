from domain.entities.Macroprocess import Macroprocess
from domain.repositories.macroprocess_repository import MacroprocessRepository

async def create_macroprocess(description: str, repository: MacroprocessRepository):
    macroprocess = Macroprocess(description=description)
    return await repository.create_macroprocess(macroprocess)

async def get_macroprocess(macroprocess_id: int, repository: MacroprocessRepository):
    return await repository.get_macroprocess(macroprocess_id)

async def get_all_macroprocesses(repository: MacroprocessRepository):
    return await repository.get_all_macroprocesses()

async def update_macroprocess(macroprocess_id: int, description: str, repository: MacroprocessRepository):
    macroprocess = Macroprocess(id=macroprocess_id, description=description)
    return await repository.update_macroprocess(macroprocess_id, macroprocess)

async def delete_macroprocess(macroprocess_id: int, repository: MacroprocessRepository):
    return await repository.delete_macroprocess(macroprocess_id)