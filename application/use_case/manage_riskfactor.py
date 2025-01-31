from domain.entities.Risk_Factor import Risk_Factory
from domain.repositories.risk_factor_repository import RiskFactorRepository

async def create_risk_factor(risk_factor_data: Risk_Factory, repository: RiskFactorRepository) -> Risk_Factory:
    return await repository.create_risk_factor(risk_factor_data)

async def get_risk_factor(risk_factor_id: int, repository: RiskFactorRepository) -> Risk_Factory:
    return await repository.get_risk_factor(risk_factor_id)

async def get_all_risk_factors(repository: RiskFactorRepository) -> list[Risk_Factory]:
    return await repository.get_all_risk_factors()

async def update_risk_factor(risk_factor_id: int, risk_factor_data: Risk_Factory, repository: RiskFactorRepository) -> Risk_Factory:
    return await repository.update_risk_factor(risk_factor_id, risk_factor_data)

async def delete_risk_factor(risk_factor_id: int, repository: RiskFactorRepository) -> None:
    await repository.delete_risk_factor(risk_factor_id)