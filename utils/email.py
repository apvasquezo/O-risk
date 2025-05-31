import smtplib
import random
import string
from email.message import EmailMessage
from config import settings 


def generar_contraseña(longitud: int = 10) -> str:
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(caracteres, k=longitud))

def enviar_correo(destinatario: str, nueva_contraseña: str):
    remitente = settings.EMAIL_ADDRESS 
    clave_app = settings.EMAIL_PASSWORD  

    
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

    try:
     
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, clave_app)  
            servidor.send_message(mensaje)
            print(f"Correo enviado exitosamente a {destinatario}")
    except smtplib.SMTPAuthenticationError as e:

        raise Exception(f"Error de autenticación al enviar el correo: {str(e)}")
    except smtplib.SMTPConnectError as e:
       
        raise Exception(f"Error de conexión al servidor SMTP: {str(e)}")
    except Exception as e:
        
        raise Exception(f"Error al enviar el correo: {str(e)}")
