from typing import Optional
from pydantic import BaseModel

class Risk_Control_Type(BaseModel):
    id_controltype:Optional[int] = None
    description:str