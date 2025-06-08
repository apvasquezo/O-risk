from typing import Optional
from pydantic import BaseModel

class Event(BaseModel):
    id_event:Optional[int]=None
    risk_type_id:int
    factor_id:int
    description:str
    probability_id:int
    impact_id:int
    
class RiskInherente(BaseModel):
    id_event:int
    description:str
    probability_id:int
    impact_id:int