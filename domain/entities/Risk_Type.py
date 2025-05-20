from typing import Optional
from pydantic import BaseModel

class Risk_type(BaseModel):
    id_risktype:Optional[int]=None
    category_id:int
    description:str