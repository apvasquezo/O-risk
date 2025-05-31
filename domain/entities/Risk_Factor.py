from typing import Optional
from pydantic import BaseModel

class Risk_Factory(BaseModel):
    id_factor:Optional[int]=None
    risk_type_id:int
    description:str