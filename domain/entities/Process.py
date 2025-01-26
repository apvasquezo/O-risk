from typing import Optional
from pydantic import BaseModel

class Process(BaseModel):
    id:Optional[int]=None
    macroprocess_id:int
    description:str