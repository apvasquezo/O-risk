from typing import Optional
from pydantic import BaseModel

class Risk_Category(BaseModel):
    id:Optional[int] = None
    description:str