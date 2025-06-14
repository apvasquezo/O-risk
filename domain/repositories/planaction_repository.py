from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Plan_action as ORMPlan
from infrastructure.orm.models import Control_action as ORMControlAction
from infrastructure.orm.models import Control as ORMControl
from domain.entities.Plan_action import Plan_action as PlanEntity
from domain.entities.Plan_action import PlanAction

class PlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 
    
    async def create_plan(self, plan:PlanEntity)-> PlanEntity:
        stmt=insert(ORMPlan).values(
            description=plan.description,
            star_date=plan.star_date,
            end_date=plan.end_date,
            personal_id=plan.personal_id,
            state=plan.state,
        ).returning(
            ORMPlan.id_plan,
            ORMPlan.description,
            ORMPlan.star_date,
            ORMPlan.end_date,
            ORMPlan.personal_id,
            ORMPlan.state,
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
                    state=row.state,
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
    
    async def get_all_plan(self)->List[PlanAction]:
        print ("entre al repositorio")
        stmt = (select(ORMPlan.id_plan,
               ORMPlan.description,
               ORMPlan.star_date,
               ORMPlan.end_date,
               ORMPlan.personal_id,
               ORMPlan.state,
               ORMControl.id_control.label("control_id"),
               ORMControl.description.label("control_name"))
        .join(ORMControlAction, ORMPlan.id_plan == ORMControlAction.action_id)  # Relación con tabla intermedia
        .join(ORMControl, ORMControlAction.control_id == ORMControl.id_control)  # Relación con tabla Control
        )
        result = await self.session.execute(stmt)
        rows= result.fetchall()
        return [
            PlanAction(
                id_plan=row.id_plan,
                description=row.description,
                star_date=row.star_date,
                end_date=row.end_date,
                personal_id=row.personal_id,
                state=row.state,
                control_id=row.control_id,
                control_name=row.control_name,
            ) for row in rows         
        ]
        
    async def update_plan(self,plan_id:int, plan:PlanEntity)-> Optional[PlanEntity]:
        print("ingreso a update ", plan_id)
        stmt = update(ORMPlan).where(ORMPlan.id_plan == plan_id).values(
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
                id_plan=row.id_plan,
                description=row.description,
                star_date=row.star_date,
                end_date=row.end_date,
                personal_id=row.personal_id,
                state=row.state
            )
        return None
    
    async def delete_plan(self, plan_id:int)->None:
        print("Intentando eliminar plan con id ", plan_id)
        # Primero elimina las relaciones en la tabla intermedia
        stmt_intermedia = delete(ORMControlAction).where(ORMControlAction.action_id == plan_id)
        await self.session.execute(stmt_intermedia)        
        # Luego elimina el plan
        stmt = delete(ORMPlan).where(ORMPlan.id_plan == plan_id)
        result= await self.session.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Plan action with ID {plan_id} not found")
        
        await self.session.commit()