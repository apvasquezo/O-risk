from pydantic import BaseModel
from typing import Optional

class Consequence(BaseModel):
    id_consequence:Optional[int]=None
    descripcion:str
    risk_factor_id:int
    even_id:int