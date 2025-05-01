from pydantic import BaseModel
from typing import Optional

class Controller(BaseModel):
    id_control:Optional[int]=None
    description:str
    frequency:Optional[str]
    control_type_id:int
    responsible_id:int    