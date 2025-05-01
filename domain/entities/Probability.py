from typing import Optional
from pydantic import BaseModel

class Probability(BaseModel):
    level:int
    description:str
    definition:str
    criteria_porcentage:int