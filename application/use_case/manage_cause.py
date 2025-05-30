from domain.entities.Cause import Causes
from domain.repositories.cause_repository import CauseRepository

async def create_cause(cause_data:Causes, repository:CauseRepository):
    return await repository.create_cause(cause_data)

async def get_cause(cause_id:int, repository:CauseRepository):
    return await repository.get_cause(cause_id)

async def get_all_cause(repository:CauseRepository):
    return await repository.get_all_cause()

async def update_cause(case_id:int, cause:Causes ,repository:CauseRepository):
    return await repository.update_causes(case_id, cause)

async def delete_cause(case_id:int, repository:CauseRepository):
    return await repository.delete_cause(case_id)