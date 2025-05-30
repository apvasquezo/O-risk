from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete
from infrastructure.orm.models import Control_action as ORMControlAction
from domain.entities.Control_action import Control_action as ControlActionEntity

class PlanControlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 
        
    async def create_planControl(self, planControl:ControlActionEntity)->ControlActionEntity:
        stmt=insert(ORMControlAction).values(
            control_id=planControl.control_id,
            action_id=planControl.action_id,
        ).returing(
            ORMControlAction.control_id,
            ORMControlAction.action_id,
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return ControlActionEntity(
                    control_id=row.control_id,
                    action_id=row.action_id,
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Plan Control already exists") from e       