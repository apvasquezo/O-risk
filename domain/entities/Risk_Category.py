from typing import Optional
from pydantic import BaseModel

class Risk_Category(BaseModel):
    id_riskcategory:Optional[int] = None
    description:str