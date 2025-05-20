from typing import Optional
from domain.entities.Personal import Personal
from domain.repositories.personal_repository import PersonalRepository

async def create_personal(personal_data: Personal, repository: PersonalRepository):
    return await repository.create_personal(personal_data)

async def get_personal(personal_id: str, repository: PersonalRepository):
    return await repository.get_personal(personal_id)

async def get_all_personal(repository: PersonalRepository):
    return await repository.get_all_personal()

async def update_personal(personal_data, repository: PersonalRepository):
    return await repository.update_personal(personal_data)

async def delete_personal(personal_id: str, repository: PersonalRepository):
    return await repository.delete_personal(personal_id)