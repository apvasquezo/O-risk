from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    id:Optional[int]=None
    name:str
    state:bool