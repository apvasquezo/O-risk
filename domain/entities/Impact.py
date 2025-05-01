from typing import Optional
from pydantic import BaseModel

class Impact(BaseModel):
    level:int
    description:str
    definition:str
    criteria_smlv:int