from domain.entities.Risk_Control_Type import Risk_Control_Type
from domain.repositories.risk_control_type_repository import RiskControlTypeRepository

async def create_risk_control_type(control_type_data: Risk_Control_Type, repository: RiskControlTypeRepository) -> Risk_Control_Type:
    return await repository.create_risk_control_type(control_type_data)

async def get_risk_control_type(control_type_id: int, repository: RiskControlTypeRepository) -> Risk_Control_Type:
    return await repository.get_risk_control_type(control_type_id)

async def get_all_risk_control_types(repository: RiskControlTypeRepository) -> list[Risk_Control_Type]:
    return await repository.get_all_risk_control_types()

async def update_risk_control_type(control_type_id: int, control_type_data: Risk_Control_Type, repository: RiskControlTypeRepository) -> Risk_Control_Type:
    return await repository.update_risk_control_type(control_type_id, control_type_data)

async def delete_risk_control_type(control_type_id: int, repository: RiskControlTypeRepository) -> None:
    await repository.delete_risk_control_type(control_type_id)