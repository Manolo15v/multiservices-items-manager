import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from app.core.config import settings 

def generate_verification_code():
    return str(random.randint(1000, 9999)) # 4 digitos

def send_email(destinatario: str, asunto: str, cuerpo_html: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SENDER_EMAIL
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(cuerpo_html, 'html')) 

        print(f"Conectando SMTP para enviar a {destinatario}...")
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls() 
        server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SENDER_EMAIL, destinatario, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

def send_verification_email(destinatario: str, code: str):
    body = f"""
    <html>
      <body>
        <h2>Verifica tu cuenta</h2>
        <p>Tu codigo de verificacion es: <b>{code}</b></p>
      </body>
    </html>
    """
    return send_email(destinatario, "Valida tu cuenta - Codigo de Verificacion", body)

def send_reset_password_email(destinatario: str, code: str):
    body = f"""
    <html>
      <body>
        <h2>Recuperación de Contraseña</h2>
        <p>Has solicitado restablecer tu contraseña.</p>
        <p>Tu código de recuperacion es: <b>{code}</b></p>
        <p>Si no fuiste tu, ignora este mensaje.</p>
      </body>
    </html>
    """
    return send_email(destinatario, "Recuperar Contraseña - Codigo", body)