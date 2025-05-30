from pydantic import BaseModel, EmailStr

class RecoveryRequest(BaseModel):
    username: str 
    email: EmailStr 