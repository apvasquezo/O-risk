from pydantic import BaseModel

class PlanStateCount(BaseModel):
    state: str
    cantidad: int