from typing import Optional
from pydantic import BaseModel

class Process(BaseModel):
    id_process:Optional[int]=None
    macroprocess_id:int
    description:str
    personal_id:str