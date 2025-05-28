from pydantic import BaseModel
from typing import Optional

class Causes(BaseModel):
    id_cause:Optional[int]=None
    description:str
