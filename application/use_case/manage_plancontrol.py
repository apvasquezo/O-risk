from domain.entities.Control_action import Control_action
from domain.repositories.plancontrol_repository import PlanControlRepository

async def create_plan_control(plancontrol_data:Control_action,repository: PlanControlRepository )-> Control_action:
    return await repository.create_planControl(plancontrol_data)

