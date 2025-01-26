from typing import Optional
from pydantic import BaseModel

class Risk_type(BaseModel):
    id:Optional[int]=None
    risk_category_id:int
    description:str