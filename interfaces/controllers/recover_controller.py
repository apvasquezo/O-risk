from fastapi import APIRouter, HTTPException, status, Depends
from utils.email import enviar_correo, generar_contraseña
from utils.schemas import RecoveryRequest
from infrastructure.orm.models import User
from infrastructure.database.db_config import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

@router.put("/recoverpassword", status_code=status.HTTP_200_OK)
async def recover_password(data: RecoveryRequest, db: AsyncSession = Depends(get_async_session)):
    try:
        # Buscar el usuario por nombre de usuario
        result = await db.execute(select(User).filter(User.username == data.username))
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Generar la nueva contraseña
        nueva_contraseña = generar_contraseña()

        # Actualizar la contraseña en la base de datos
        user.password = nueva_contraseña
        await db.commit()

        # Enviar el correo con la nueva contraseña
        enviar_correo(data.email, nueva_contraseña)

        return {"message": f"Se ha enviado una nueva contraseña a {data.email}."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")