from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    id_role:Optional[int]=None
    name:str
    state:bool