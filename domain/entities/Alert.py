from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Causes(BaseModel):
    id_alert:Optional[int]=None
    title = str 
    message = str
    is_read = bool
    date_created = datetime
    role_id = str
    type =str
    eventlog_id = int
    control_id = int