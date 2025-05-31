from typing import Optional
from pydantic import BaseModel

class Personal(BaseModel):
    id_personal: str
    name:str
    position:str
    area:Optional[str]
    email:str
    notify:bool