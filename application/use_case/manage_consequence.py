from domain.entities.Consequence import Consequence
from domain.repositories.consequence_repository import ConsequenceRepository

async def create_consequence(consequence_data:Consequence, repository:ConsequenceRepository):
    return await repository.create_consequence(consequence_data)

async def get_consequence(consequence_id:int, repository:ConsequenceRepository):
    return await repository.get_consequence(consequence_id)

async def get_all_consequence(repository:ConsequenceRepository):
    return await repository.get_all_consequence()

async def update_consequence(consequence_id:int, consequence:Consequence, repository:ConsequenceRepository):
    return await repository.update_consequence(consequence_id, consequence)

async def delete_consequence(consequence_id:int, repository:ConsequenceRepository):
    return await repository.delete_consequence(consequence_id)