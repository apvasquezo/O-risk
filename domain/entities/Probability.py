from typing import Optional
from pydantic import BaseModel

class Probability(BaseModel):
    id:Optional[int]=None
    level:int
    description:str
    definition:str
    criteria_porcentage:int