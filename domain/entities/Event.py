from typing import Optional
from pydantic import BaseModel

class Event(BaseModel):
    id:Optional[int]=None
    risk_type_id:int
    factor:str
    description:str
    probability_id:int
    impact_id:int