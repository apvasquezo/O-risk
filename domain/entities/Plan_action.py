from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Plan_action(BaseModel):
    id_plan: Optional[int]=None
    description: str
    star_date: datetime
    end_date: datetime
    personal_id: str
    state:Optional[str] 
    
class PlanAction (BaseModel):
    id_plan: Optional[int]=None
    description:str
    star_date: datetime
    end_date: datetime
    personal_id: str
    state:Optional[str] 
    control_id:int
    control_name:str  