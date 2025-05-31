from pydantic import BaseModel
from typing import Optional

class Channels(BaseModel):
    id_channel:Optional[int]=None
    description:str