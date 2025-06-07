from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Dict, Any
from infrastructure.orm.models import Plan_action as ORMPlan
from application.schemas.dashboard import PlanStateCount
from infrastructure.orm.models import Evaluation, EventLog, Process

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

    async def get_risk_heatmap_chart_data(self) -> List[Dict[str, Any]]:
        stmt = (
            select(
                Process.description.label("process_name"),
                Evaluation.n_probability,
                Evaluation.n_impact
            )
            .join(EventLog, Evaluation.eventlog_id == EventLog.id_eventlog)
            .join(Process, EventLog.process_id == Process.id_process)
        )

        result = await self.session.execute(stmt)
        rows = result.fetchall()

        temp_data = {}

        for row in rows:
            nivel_riesgo = row.n_probability * row.n_impact
            proceso = row.process_name

            # Clasificación normativa
            if nivel_riesgo <= 2:
                nivel = "Muy Bajo"
            elif nivel_riesgo <= 4:
                nivel = "Bajo"
            elif nivel_riesgo <= 9:
                nivel = "Medio"
            elif nivel_riesgo <= 16:
                nivel = "Alto"
            else:
                nivel = "Muy Alto"

            if nivel not in temp_data:
                temp_data[nivel] = {}

            if proceso not in temp_data[nivel]:
                temp_data[nivel][proceso] = 0

            temp_data[nivel][proceso] += 1

        all_processes = sorted(set(p for lvl in temp_data.values() for p in lvl))

        chart_data = []
        for nivel in ["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"]:
            serie = {
                "name": nivel,
                "data": [
                    {"x": proceso, "y": temp_data.get(nivel, {}).get(proceso, 0)}
                    for proceso in all_processes
                ]
            }
            chart_data.append(serie)

        return chart_data
