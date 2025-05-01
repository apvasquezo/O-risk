from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Plan_action(BaseModel):
    id_plan = Optional[int]=None
    description=str
    star_date = datetime
    end_date = datetime
    personal_id = int
    state=Optional[str] 