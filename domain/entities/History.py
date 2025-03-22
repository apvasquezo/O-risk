from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    id:Optional[int]=None
    eventLog_id:int
    control_id:int
    start_date:datetime
    end_date:Optional[datetime]
    value_risk:float    