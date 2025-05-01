from typing import Optional
from pydantic import BaseModel

class Macroprocess(BaseModel):
    id_macro: Optional[int]=None
    description:str