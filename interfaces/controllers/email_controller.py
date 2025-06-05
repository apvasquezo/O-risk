from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from utils.notify_email import send_email
from utils.auth import role_required

router = APIRouter(
    prefix="/email", 
    tags=["Email"],
     dependencies=[Depends(role_required("admin"))]
    )

class EmailRequest(BaseModel):
    email_send: str
    description: str
    personal:str

@router.post("/")
async def send_email_route(data: EmailRequest):
    print("Los datos del email ", data)
    try:
        send_email(data.email_send, data.description, data.personal)
        return {"message": f"Correo enviado a {data.email_send}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
