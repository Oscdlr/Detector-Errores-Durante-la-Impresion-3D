# Importo las librerias necesarias para enviar el correo
import smtplib
from email.mime.multipart import MIMEMultipart # Para crear el correo electronico
from email.mime.text import MIMEText # Para crear el mensaje de texto

# Gestiono el envio de correos electronico cuando detecta error
class GestorErrores:
    def __init__(self, correo_origen, contrasena, servidor_smtp='smtp.dominio.com', puerto=587):
        self.correo_origen = correo_origen
        self.contrasena = contrasena
        self.servidor_smtp = servidor_smtp # Protocolo estandar envio emails "Simple Mail Transfer Protocol"
        self.puerto = puerto

    # Funcion que se encarga del envio del correo al destinatario informando del error.
    def enviar_correo(self, correo_destino, coincidencia):
        # Configuro del servidor SMTP
        servidor_smtp = 'smtp.gmail.com' # servidor de gmail
        puerto_smtp = 587 # Puerto estandar de entrega de correo
        usuario = self.correo_origen
        contrasena = self.contrasena

        # Creo el mensaje con asunto y cuerpo
        asunto = 'Alerta de error en comparación de contornos'
        cuerpo = f'ERROR DETECTADO: La coincidencia es {coincidencia}'

        msg = MIMEMultipart()
        msg['From'] = usuario
        msg['To'] = correo_destino
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain')) # Envio como texto plano

        try:
            # Conecto conel servidor SMTP
            servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
            servidor.starttls() # comando para cambiar a conexion segura
            servidor.login(usuario, contrasena) # login en gmail
            servidor.send_message(msg) # Envio de mensaje
            servidor.quit()
            print("Correo enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
