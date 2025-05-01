from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Evaluation(BaseModel):
    id_evaluation:Optional[int]=None
    control_id=int
    event_id=int
    eval_date=datetime
    n_probability=int
    n_impact=int
    personal_id = int
    next_date = datetime
    description=str
    state=Optional[str] 