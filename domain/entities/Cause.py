from pydantic import BaseModel
from typing import Optional

class Causes(BaseModel):
    id_cause:Optional[int]=None
    descripcion:str
    risk_factor_id:int
    even_id:int