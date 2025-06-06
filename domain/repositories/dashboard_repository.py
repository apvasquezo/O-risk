from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List
from infrastructure.orm.models import Plan_action as ORMPlan
from domain.entities.Plan_action import Plan_action
import domain.entities.Plan_action as pa
class PlanDRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 

    async def get_all_plan(self)->List[Plan_action]:
        print ("entre al repositorio")
        stmt = select(ORMPlan.state,
        )
        result = await self.session.execute(stmt)
        rows= result.fetchall()
        return [
            Plan_action(
                state=row.state,                
            ) for row in rows         
        ]   
    
