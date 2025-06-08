from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy import func
from infrastructure.orm.models import Plan_action as ORMPlan
from infrastructure.orm.models import Event as ORMInherente
from infrastructure.orm.models import Evaluation as ORMResidual
from domain.entities.Plan_action import PlanStateCount
from domain.entities.Event import RiskInherente
from domain.entities.Evaluation import Evalrisk

class PlanDRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_plan(self) -> List[PlanStateCount]:
        stmt = select(ORMPlan.state, func.count().label("cantidad")).group_by(ORMPlan.state)
        result = await self.session.execute(stmt)
        rows = result.fetchall()
        return [
            PlanStateCount(state=row.state, cantidad=row.cantidad)
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
        print("La consulta ", stmt)
        result = await self.session.execute(stmt)
        print("La respuesta ", result)
        rows = result.all()
        return [
            Evalrisk(
                eventlog_id=row[0],
                n_probability=row[1],
                n_impact=row[2],
            ) for row in rows
        ]  
        
