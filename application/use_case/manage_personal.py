from typing import Optional
from domain.entities.Personal import Personal
from domain.repositories.personal_repository import PersonalRepository

async def create_personal(name: str, position: str, area: Optional[str], process_id: Optional[int], email: Optional[str], repository: PersonalRepository):
    personal = Personal(name=name, position=position, area=area, process_id=process_id, email=email)
    return await repository.create_personal(personal)

async def get_personal(personal_id: int, repository: PersonalRepository):
    return await repository.get_personal(personal_id)

async def get_all_personal(repository: PersonalRepository):
    return await repository.get_all_personal()

async def update_personal(personal_id: int, name: str, position: str, area: Optional[str], process_id: Optional[int], email: Optional[str], repository: PersonalRepository):
    personal = Personal(id=personal_id, name=name, position=position, area=area, process_id=process_id, email=email)
    return await repository.update_personal(personal)

async def delete_personal(personal_id: int, repository: PersonalRepository):
    return await repository.delete_personal(personal_id)