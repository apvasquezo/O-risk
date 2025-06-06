from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from infrastructure.database.db_config import get_async_session
from utils.auth import role_required
from typing import List
from domain.repositories.dashboard_repository import PlanDRepository
from pydantic import BaseModel

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(role_required("admin"))]
)

class PlanResponse(BaseModel):
    state:str


@router.get("/", response_model=List[PlanResponse])
async def read_all_plan(db: AsyncSession = Depends(get_async_session)):
    repository = PlanDRepository(db)
    plan_type = await repository.get_all_plan()
    return [PlanResponse(**p.model_dump()) for p in plan_type]