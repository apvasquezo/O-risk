from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy import func, literal_column, case, cast, Float
from infrastructure.orm.models import Plan_action as ORMPlan
from infrastructure.orm.models import Event as ORMInherente
from infrastructure.orm.models import Evaluation as ORMResidual
from domain.entities.Plan_action import PlanStateCount, ComplianceResult
from domain.entities.Event import RiskInherente
from domain.entities.Evaluation import Evalrisk, KriFrequency

class PlanDRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_plan(self) -> List[PlanStateCount]:
        stmt = select(ORMPlan.state, func.count().label("amount")).group_by(ORMPlan.state)
        result = await self.session.execute(stmt)
        rows = result.fetchall()
        return [
            PlanStateCount(state=row.state, amount=row.amount)
            for row in rows
        ]
    
    async def get_inherente(self) -> List[RiskInherente]:
        stmt = select( ORMInherente.id_event, ORMInherente.description, ORMInherente.probability_id, ORMInherente.impact_id)
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            RiskInherente(
                id_event=row[0],
                description=row[1],
                probability_id=row[2],
                impact_id=row[3],
            ) for row in rows
        ]   

    async def get_residual(self) -> List[Evalrisk]:
        stmt = select(ORMResidual.eventlog_id, ORMResidual.n_probability, ORMResidual.n_impact)
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            Evalrisk(
                eventlog_id=row[0],
                n_probability=row[1],
                n_impact=row[2],
            ) for row in rows
        ]  

    async def get_eval_control(self) -> List[PlanStateCount]:
        stmt = select(ORMResidual.control_efficiency, func.count().label("amount")).group_by(ORMResidual.control_efficiency)
        result = await self.session.execute(stmt) 
        print("la consulta ", stmt)     
        rows = result.fetchall()
        state_map = {
                0.20: "Critica",
                0.50: "Baja",
                0.80: "Eficiente",
                1: "Alta"
            }
        return [
            PlanStateCount(state=state_map.get(float(row.control_efficiency)), amount=row.amount)
            for row in rows
        ]                

    async def get_eval_frequency(self) -> List[KriFrequency]:
        stmt = (
            select(
                func.date_trunc(literal_column("'month'"), ORMResidual.eval_date).label("periodo"),
                func.count().label("cantidad")
            )
            .group_by(func.date_trunc(literal_column("'month'"), ORMResidual.eval_date))
            .order_by(func.date_trunc(literal_column("'month'"), ORMResidual.eval_date))
        )
        result = await self.session.execute(stmt)
        rows = result.fetchall()
        return [{"periodo": row.periodo.strftime("%Y-%m"), "cantidad": row.cantidad} for row in rows]
    

    async def get_cumplimiento(self) -> List[ComplianceResult]:
        stmt = (
            select(ORMPlan.personal_id.label("responsible"),
                ( cast(
                        func.count().filter(ORMPlan.state.in_(['Completado', 'En progreso'])),
                        Float
                    ) / func.count()
                ).label("cumplimiento")
            )
            .group_by(ORMPlan.personal_id)
            .order_by(ORMPlan.personal_id)
        )
        print("la consulta de compliance ", stmt)
        result = await self.session.execute(stmt)
        rows = result.fetchall()       
        return [
            ComplianceResult(
                responsible=row.responsible,
                cumplimiento=round(row.cumplimiento or 0, 2)
            )
            for row in rows
        ]
