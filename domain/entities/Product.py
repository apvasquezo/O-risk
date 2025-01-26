from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id:Optional[int]=None
    description:str