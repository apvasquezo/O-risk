from typing import Optional
from pydantic import BaseModel
from datetime import date

class Plan_action(BaseModel):
    id_plan: Optional[int]=None
    description: str
    star_date: date
    end_date: date
    personal_id: str
    state:Optional[str] 
    
class PlanAction (BaseModel):
    id_plan: Optional[int]=None
    description:str
    star_date: date
    end_date: date
    personal_id: str
    state:Optional[str] 
    control_id:int
    control_name:str  
    
class PlanStateCount(BaseModel):
    state: str
    amount: int
    
class ComplianceResult(BaseModel):
    responsible: str
    cumplimiento: float