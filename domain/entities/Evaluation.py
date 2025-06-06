from typing import Optional
from pydantic import BaseModel
from datetime import date

class Evaluation(BaseModel):
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