from pydantic import BaseModel
from typing import Optional
from datetime import date

class EventLog(BaseModel):
    id_eventlog: Optional[int]=None
    event_id: int
    description:str
    start_date: date
    end_date: Optional[date] 
    discovery_date: Optional[date] 
    accounting_date: Optional[date]
    amount: Optional[float] 
    recovered_amount: Optional[float] 
    insurance_recovery: Optional[float]
    acount: Optional[float]
    product_id: int 
    process_id: int 
    channel_id: int 
    city: Optional[str] 
    responsible_id: str 
    status: Optional[str] 
    cause1_id: int
    cause2_id: Optional[int]
    conse1_id: int
    conse2_id: Optional[int]