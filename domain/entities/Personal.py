from typing import Optional
from pydantic import BaseModel

class Personal(BaseModel):
    id_personal: str
    name:str
    post:str
    area:Optional[str]
    email:str