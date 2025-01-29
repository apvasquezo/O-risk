from domain.entities.Risk_Type import Risk_Type
from domain.repositories.risk_type_repository import RiskTypeRepository

async def create_risk_type(risk_type_data: Risk_Type, repository: RiskTypeRepository) -> Risk_Type:
    return await repository.create_risk_type(risk_type_data)

async def get_risk_type(risk_type_id: int, repository: RiskTypeRepository) -> Risk_Type:
    return await repository.get_risk_type(risk_type_id)

async def get_all_risk_types(repository: RiskTypeRepository) -> list[Risk_Type]:
    return await repository.get_all_risk_types()

async def update_risk_type(risk_type_id: int, risk_type_data: Risk_Type, repository: RiskTypeRepository) -> Risk_Type:
    return await repository.update_risk_type(risk_type_id, risk_type_data)

async def delete_risk_type(risk_type_id: int, repository: RiskTypeRepository) -> None:
    await repository.delete_risk_type(risk_type_id)