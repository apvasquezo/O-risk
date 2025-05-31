from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.planaction_repository import PlanRepository
from application.use_case.manage_plan import (
    create_plans,
    get_plan,
    get_all_plans,
    update_plans,
    delete_plans,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/plans",
    tags=["Planes de Accion"],
    dependencies=[Depends(role_required("admin"))]
)

class PlanActionCreate (BaseModel):
    description:str
    star_date: datetime
    end_date: datetime
    personal_id: str
    state:Optional[str]

class PlanActionResponse (BaseModel):
    id_plan: Optional[int]=None
    description:str
    star_date: datetime
    end_date: datetime
    personal_id: str
    state:Optional[str] 

class PlanActionResponseC (BaseModel):
    id_plan: Optional[int]=None
    description:str
    star_date: datetime
    end_date: datetime
    personal_id: str
    state:Optional[str] 
    control_id:int
    control_name:str   
    
@router.post("/", response_model=PlanActionResponse, status_code=201)
async def create_plan_action_endpoint(plan_type: PlanActionCreate, db: AsyncSession = Depends(get_async_session)):
    repository =PlanRepository(db)
    created = await create_plans(plan_type, repository)
    return PlanActionResponse(**created.model_dump())

@router.get("/{plan_id}", response_model=PlanActionResponse)
async def read_plan(plan_id:int, db: AsyncSession = Depends(get_async_session)):
    repository = PlanRepository(db)
    plan_type = await get_plan(plan_id, repository)
    if not plan_type:
        raise HTTPException(status_code=404, detail="Tipo de plan no encontrado")
    return PlanActionResponse(**plan_type.model_dump())

@router.get("/", response_model=List[PlanActionResponseC])
async def read_all_plan(db: AsyncSession = Depends(get_async_session)):
    repository = PlanRepository(db)
    plan_type = await get_all_plans(repository)
    print ("trae del repo ", plan_type)   
    return [PlanActionResponseC(**p.model_dump()) for p in plan_type]

@router.put("/{plan_id}", response_model=PlanActionResponse)
async def update_plan_endpoint(plan_id:int, plan_type:PlanActionCreate, db: AsyncSession = Depends(get_async_session)):
    repository = PlanRepository(db)
    updated = await update_plans(plan_id, plan_type, repository)
    if not updated:
        raise HTTPException(status_code=404, detail="Tipo de plan no encontrado")
    return PlanActionResponse(**updated.model_dump())

@router.delete("/{plan_id}", response_model=PlanActionResponse)
async def delete_plan_endpoint(plan_id:int, db: AsyncSession = Depends(get_async_session)):
    repository = PlanRepository(db)
    plan_type = await delete_plans(plan_id, repository)
    if not plan_type:
        raise HTTPException(status_code=404, detail="Tipo de plan no encontrado")
    return PlanActionResponse(**plan_type.model_dump())
