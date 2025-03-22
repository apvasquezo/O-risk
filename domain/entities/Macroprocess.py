from typing import Optional
from pydantic import BaseModel

class Macroprocess(BaseModel):
    id: Optional[int]=None
    description:str