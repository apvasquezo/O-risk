from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from infrastructure.database.db_config import get_async_session
from application.schemas.dashboard import PlanStateCount
from domain.repositories.dashboard_repository import PlanDRepository
from pydantic import BaseModel

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

class PlanResponse(BaseModel):
    state: str

# Endpoint para planes de acción por estado
@router.get("/", response_model=List[PlanStateCount])
async def read_all_plan(db: AsyncSession = Depends(get_async_session)):
    repository = PlanDRepository(db)
    return await repository.get_all_plan()

# Endpoint para el mapa de calor de riesgos por proceso
@router.get("/risk-heatmap")
async def get_heatmap_chart_data(db: AsyncSession = Depends(get_async_session)):
    repository = PlanDRepository(db)
    return await repository.get_risk_heatmap_chart_data()
