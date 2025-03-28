from domain.entities.Impact import Impact
from domain.repositories.impact_repository import ImpactRepository

async def create_impact(impact_data: Impact, repository: ImpactRepository) -> Impact:
    return await repository.create_impact(impact_data)

async def get_impact(impact_id: int, repository: ImpactRepository) -> Impact:
    return await repository.get_impact(impact_id)

async def get_all_impacts(repository: ImpactRepository) -> list[Impact]:
    return await repository.get_all_impacts()

async def update_impact(impact_id: int, impact_data: Impact, repository: ImpactRepository) -> Impact:
    return await repository.update_impact(impact_id, impact_data)

async def delete_impact(impact_id: int, repository: ImpactRepository) -> None:
    await repository.delete_impact(impact_id)