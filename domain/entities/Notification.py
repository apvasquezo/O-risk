from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Notification(BaseModel):
    id: Optional[int]=None
    message:str
    suggestion_control:str
    date_send:datetime
    user_id:int
    eventLog_id:int