from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from utils.auth import role_required
from typing import List
import logging
from domain.repositories.dashboard_repository import PlanDRepository
from pydantic import BaseModel

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(role_required("admin"))]
)

class PlanStateCount(BaseModel):
    state:str
    amount: int

class RiskInherente(BaseModel):
    id_event:int
    description:str
    probability_id:int
    impact_id:int

class RiskResidual(BaseModel):
    eventlog_id: int 
    n_probability: int
    n_impact: int
    
class KriFrequency(BaseModel):
    periodo: str
    cantidad: int
    
class ComplianceResult(BaseModel):
    responsible: str
    cumplimiento: float

# Endpoint para planes de acción por estado
@router.get("/plan", response_model=List[PlanStateCount])
async def read_all_plan(db: AsyncSession = Depends(get_async_session)):
    repository = PlanDRepository(db)
    return await repository.get_all_plan()

@router.get("/efficiency", response_model=List[PlanStateCount])
async def read_all_efficiency(db: AsyncSession = Depends(get_async_session)):
    try:
        repository = PlanDRepository(db)
        return await repository.get_eval_control()
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_all_efficiency: {str(e)}")    

@router.get("/frequency", response_model=List[KriFrequency])
async def read_control_frequency(db: AsyncSession = Depends(get_async_session)):
    try:
        repository = PlanDRepository(db)
        return await repository.get_eval_frequency()
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_control_frecuency: {str(e)}")      

@router.get("/inherente", response_model=List[RiskInherente])
async def read_inherente(db: AsyncSession = Depends(get_async_session)):
    try:
        repository= PlanDRepository(db)
        risk_in= await repository.get_inherente()
        return [RiskInherente(
            id_event=e.id_event,
            description=e.description, 
            probability_id=e.probability_id, 
            impact_id=e.impact_id) for e in risk_in]
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_inherente: {str(e)}")
        
@router.get("/residual", response_model=List[RiskResidual])
async def read_residual(db: AsyncSession = Depends(get_async_session)):
    try:
        repository= PlanDRepository(db)
        risk_re= await repository.get_residual()   
        return [ RiskResidual (
            eventlog_id= e.eventlog_id,
            n_probability= e.n_probability,
            n_impact= e.n_impact,
        ) for e in risk_re]     
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_residual: {str(e)}")


@router.get("/compliance", response_model=List[ComplianceResult])
async def get_compliance(db: AsyncSession = Depends(get_async_session)):
    try:
        repository= PlanDRepository(db) 
        return await repository.get_cumplimiento()
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en get_compliance: {str(e)}")
