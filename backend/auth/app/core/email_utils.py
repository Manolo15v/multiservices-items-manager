import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from app.core.config import settings 

def generate_verification_code():
    return str(random.randint(1000, 9999)) #4 digitos

def send_verification_email(destinatario: str, code: str):
    try:
        #configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = settings.SENDER_EMAIL
        msg['To'] = destinatario
        msg['Subject'] = "Valida tu cuenta - Codigo de Verificacion"

        body = f"""
        <html>
          <body>
            <h2>Bienvenido a nuestra App</h2>
            <p>Tu codigo de verificacion es: <b>{code}</b></p>
            <p>Por favor ingresalo en la pagina de validacion.</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html')) 

        #conexion al servidor SMTP
        print("Conectando al servidor SMTP...")
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls() 
        server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SENDER_EMAIL, destinatario, text)
        server.quit()
        
        print(f"Correo enviado exitosamente a {destinatario}")
        return True
        
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False