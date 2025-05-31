
from pydantic import BaseModel
from typing import Optional

class UserUpdateDTO(BaseModel):
    username: Optional[str]  
    new_password: Optional[str] 
