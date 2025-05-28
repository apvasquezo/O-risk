# utils/email.py

import smtplib
import random
import string
from email.message import EmailMessage

def generar_contraseña(longitud: int = 10) -> str:
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(caracteres, k=longitud))

def enviar_correo(destinatario: str, nueva_contraseña: str):
    remitente = "elizaesco20240812@gmail.com"
    clave_app = "kycorrerxxmiwdfnrwh​​"

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

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, clave_app)
        servidor.send_message(mensaje)

import bcrypt

def hashear_contraseña(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')