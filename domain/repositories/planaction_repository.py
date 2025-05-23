from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Plan_action as ORMPlan
from domain.entities.Plan_action import Plan_action as PlanEntity
class PlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_plan(self, plan:PlanEntity)-> PlanEntity:
        stmt=insert(ORMPlan).values(
            description=plan.description,
            star_date=plan.star_date,
            end_date=plan.end_date,
            personal_id=plan.personal_id,
            state=plan.state
        ).returing(
            ORMPlan.id_plan,
            ORMPlan.description,
            ORMPlan.star_date,
            ORMPlan.end_date,
            ORMPlan.personal_id,
            ORMPlan.state
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return PlanEntity(
                    id_plan=row.id_plan,
                    description=row.description,
                    star_date=row.star_date,
                    end_date=row.end_date,
                    personal_id=row.personal_id,
                    state=row.state
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Plan of action already exists") from e
        
    async def get_plan(self, plan_id:int)->Optional[PlanEntity]:
        stmt = select(ORMPlan).where(ORMPlan.id_plan == plan_id)
        result = await self.session.execute(stmt)
        plan= result.scalar_one_or_none()
        if plan:
            return PlanEntity(
                id_plan=plan.id_plan,
                description=plan.description,
                star_date=plan.star_date,
                end_date=plan.end_date,
                personal_id=plan.personal_id,
                state=plan.state
            )
        return None
    
    async def get_all_plan(self)->List[PlanEntity]:
        stmt = select(ORMPlan)
        result = await self.session.execute(stmt)
        plans = result.scalars().all()
        return [
            PlanEntity(
                id_plan=plans.id_plan,
                description=plans.description,
                star_date=plans.star_date,
                end_date=plans.end_date,
                personal_id=plans.personal_id,
                state=plans.state
            ) for c in plans
        ]
        
    async def update_plan(self,plan_id:int, plan:PlanEntity)-> Optional[PlanEntity]:
        stmt = update(ORMPlan).where(plan.id_plan == plan_id).values(
            description=plan.description,
            star_date=plan.star_date,
            end_date=plan.end_date,
            personal_id=plan.personal_id,
            state=plan.state
        ).returning(
            ORMPlan.id_plan,
            ORMPlan.description,
            ORMPlan.star_date,
            ORMPlan.end_date,
            ORMPlan.personal_id,
            ORMPlan.state
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.fetchone()
        if row:
            return PlanEntity(
                id_plan=plan.id_plan,
                description=plan.description,
                star_date=plan.star_date,
                end_date=plan.end_date,
                personal_id=plan.personal_id,
                state=plan.state
            )
        return None
    
    async def delete_plan(self, plan_id:int)->None:
        stmt = delete(ORMPlan).where(ORMPlan.id_plan == plan_id)
        result= await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Plan of Action with id {plan_id} not found")