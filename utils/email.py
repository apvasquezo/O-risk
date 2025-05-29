import smtplib
import random
import string
from email.message import EmailMessage
from config import settings  # Importamos la instancia de configuración

def generar_contraseña(longitud: int = 10) -> str:
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(caracteres, k=longitud))

def enviar_correo(destinatario: str, nueva_contraseña: str):
    # Usamos las credenciales cargadas desde Pydantic Settings
    remitente = settings.EMAIL_ADDRESS
    clave_app = settings.EMAIL_PASSWORD

    # Asegurarse de que las variables de entorno estén configuradas correctamente
    if not remitente or not clave_app:
        raise ValueError("Las credenciales del correo no están configuradas correctamente en el archivo .env")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Recuperación de contraseña - O-risk"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(f"""
    Hola,

    Se ha generado una nueva contraseña para tu cuenta:

    Nueva contraseña: {nueva_contraseña}

    Por seguridad, cámbiala después de iniciar sesión.

    Saludos,
    Equipo O-risk
    """)

    # Conectar y enviar el correo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, clave_app)
            servidor.send_message(mensaje)
    except Exception as e:
        raise Exception(f"Error al enviar el correo: {str(e)}")