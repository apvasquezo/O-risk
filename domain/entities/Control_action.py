from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Control_action(BaseModel):
    id_controlaction:Optional[int]=None
    control_id:int
    action_id:int
    
    
    