from pydantic import BaseModel
from typing import Optional

class Consequence(BaseModel):
    id_consequence:Optional[int]=None
    description:str
