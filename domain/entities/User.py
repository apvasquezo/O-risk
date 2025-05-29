from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id_user:Optional[int]=None
    username:str
    password:str
    role_id:int
    created_at:Optional[str]=None
    updated_at:Optional[str]=None
    role_name: Optional[str] = None 