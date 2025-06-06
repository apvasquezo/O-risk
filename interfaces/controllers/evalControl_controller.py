from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from pydantic import BaseModel
from typing import Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_async_session
from domain.repositories.evaluation_repository import EvaluationRepository
from application.use_case.manage_evaluation import (
    create_evaluations,
    get_evaluations,
    get_all_evaluations,
    update_evaluations,
    delete_evaluations,
)
from utils.auth import role_required

router = APIRouter(
    prefix="/evalcontrol",
    tags=["Evaluacion Controles"],
    dependencies=[Depends(role_required("admin"))] 
)

class EvalControlCreate(BaseModel):
    eventlog_id: int   
    control_id: int
    eval_date: date
    n_probability: int
    n_impact: int
    next_date: date
    description: str
    observation: str
    state_control: str
    state_evaluation: str
    control_efficiency: float
    created_by: str  

class EvalControlResponse(BaseModel):
    id_evaluation: Optional[int]=None
    eventlog_id: int   
    control_id: int
    eval_date: date
    n_probability: int
    n_impact: int
    next_date: date
    description: str
    observation: str
    state_control: str
    state_evaluation: str
    control_efficiency: float
    created_by: str  
    
@router.post("/", response_model=EvalControlResponse, status_code=201)
async def create_eval_endpoint(evaluation: EvalControlCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EvaluationRepository(db)
        created = await create_evaluations(evaluation, repository)
        return EvalControlResponse(**created.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en create_eval_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{eval_id}", response_model=EvalControlResponse)
async def read_eval_endpoint(eval_id:int, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EvaluationRepository(db)
        evalued = await get_evaluations(eval_id, repository)
        if not evalued:
            raise HTTPException(status_code=404, detail="Registro no encontrado")           
        return EvalControlResponse(**evalued.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_eval_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=List[EvalControlResponse])
async def read_all_eval_endpoint(db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EvaluationRepository(db)
        evalues = await get_all_evaluations(repository)
        return [EvalControlResponse(**e.model_dump()) for e in evalues]
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en read_all_eval_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/{eval_id}", response_model=EvalControlResponse)
async def update_eval_endpoint(eval_id:int, evaluation: EvalControlCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EvaluationRepository(db)
        updated = await update_evaluations(eval_id, evaluation, repository)
        if not updated:
            raise HTTPException(status_code=404, detail="Registro no encontrado")           
        return EvalControlResponse(**updated.model_dump())
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en update_eval_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/{eval_id}", response_model=EvalControlResponse)
async def delete_eval_endpoint(eval_id:int, db: AsyncSession = Depends(get_async_session)):
    try:
        repository = EvaluationRepository(db)
        await delete_evaluations(eval_id, repository)
        return {"detail": "Registro eliminado"}
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {str(e)}")
    except Exception as e:
        logging.error(f"Error en delete_eval_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
