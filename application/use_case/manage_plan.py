from domain.entities.Plan_action import Plan_action
from domain.repositories.planaction_repository import PlanRepository

async def create_plans(plan_data: Plan_action, repository: PlanRepository) -> Plan_action:
    return await repository.create_plan(plan_data)

async def get_plan(plan_id: int, repository: PlanRepository) -> Plan_action:
    return await repository.get_plan(plan_id)

async def get_all_plans(repository: PlanRepository) -> list[Plan_action]:
    print ("entre al manager")
    return await repository.get_all_plan()

async def update_plans(plan_id: int, plan_data: Plan_action, repository: PlanRepository) -> Plan_action:
    return await repository.update_plan(plan_id, plan_data)

async def delete_plans(plan_id: int, repository: PlanRepository) -> None:
    await repository.delete_plan(plan_id)