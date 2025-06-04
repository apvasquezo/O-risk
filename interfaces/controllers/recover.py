from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from infrastructure.database.db_config import get_async_session
from infrastructure.orm.models import User  # <-- Este es el modelo SQLAlchemy CORRECTO
from utils.email import enviar_correo, generar_contraseña  # Usa tus funciones existentes

class RecoveryRequest(BaseModel):
    username: str
    email: EmailStr

router = APIRouter(prefix="/recoverpassword", tags=["Recuperación"])

@router.post("", status_code=status.HTTP_200_OK)
async def recuperar_contrasena(
    data: RecoveryRequest, 
    db: AsyncSession = Depends(get_async_session)
    ):

    result = await db.execute(
        select(User).where(func.lower(User.username) == data.username.lower())
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado en la base de datos."
        )

    # Generar nueva contraseña temporal
    nueva_contraseña = generar_contraseña()

    try:
        enviar_correo(data.email, nueva_contraseña)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar el correo: {str(e)}"
        )

    return {
        "message": f"Se ha enviado una nueva contraseña al correo {data.email}.",
        "nota": "Te recomendamos cambiarla al iniciar sesión."
    }