from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.event_repository import EventRepository
from application.use_case.manage_event import (
    create_event,
    get_event,
    get_all_events,
    update_event,
    delete_event,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/evalcontrol",
    tags=["Evaluacion Controles"],
    dependencies=[Depends(role_required("admin"))] 
)

class EvalControlCreate(BaseModel):
    risk_type_id: int
    factor_id: int
    description: str
    probability_id: int
    impact_id: int

class EvalControlResponse(BaseModel):
    id_event: int
    risk_type_id: int
    factor_id: int
    description: str
    probability_id: int
    impact_id: int