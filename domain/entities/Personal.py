from typing import Optional
from pydantic import BaseModel

class Personal(BaseModel):
    id: Optional[int]=None
    name:str
    post:str
    area:Optional[str]
    process_id:int
    email:str