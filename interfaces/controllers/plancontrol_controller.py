from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.plancontrol_repository import PlanControlRepository
from application.use_case.manage_plancontrol import (
    create_plan_control,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/plancontrol",
    tags=["Planes Controles"],
    dependencies=[Depends(role_required("admin"))]
)

class PlanControlCreate (BaseModel):
    control_id:int
    action_id:int
    
class PlanControlResponse (BaseModel):
    control_id:int
    action_id:int
    
@router.post("/", response_model=PlanControlResponse, status_code=201)
async def create_plancontrol(plancontrol:PlanControlCreate, db:  AsyncSession = Depends(get_async_session)):
    repository =PlanControlRepository(db)
    created= await create_plan_control(plancontrol, repository)
    return PlanControlResponse(**created.model_dump())