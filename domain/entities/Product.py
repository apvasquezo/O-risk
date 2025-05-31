from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id_product:Optional[int]=None
    description:str