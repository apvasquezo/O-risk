from pydantic import BaseModel
from typing import Optional

class Channels(BaseModel):
    id:Optional[int]=None
    descripcion:str