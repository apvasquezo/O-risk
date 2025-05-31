from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventLog(BaseModel):
    id_eventlog: Optional[int]=None
    event_id: int
    description:str
    start_date: datetime 
    end_date: Optional[datetime] 
    discovery_date: Optional[datetime] 
    accounting_date: Optional[datetime]
    amount: Optional[float] 
    recovered_amount: Optional[float] 
    insurance_recovery: Optional[float] 
    risk_factor_id: int 
    product_id: int 
    process_id: int 
    channel_id: int 
    city: Optional[str] 
    responsible_id: int 
    status: Optional[str] 