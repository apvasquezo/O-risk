import smtplib
from email.message import EmailMessage
from config import settings 

def send_email(destinatario: str, riesgo: str, personal:str):
    remitente = settings.EMAIL_ADDRESS 
    clave_app = settings.EMAIL_PASSWORD  

    
    if not remitente or not clave_app:
        raise ValueError("Revisar credenciales de correo en .env")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Nuevo Riesgo Grabado - O-risk"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(f"""
    Cordial Saludo,

    Se ha generado un nuevo riesgo en la plataforma:

    Riesgo: {riesgo}
    Generado por: {personal}

    Para conocer mayor información ingrese al sistema con sus credenciales.

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