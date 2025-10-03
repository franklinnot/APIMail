from base64 import b64decode
from PIL import Image
from io import BytesIO
import uuid
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .classes import Respuesta, SMPTConfig
from .dtos import Notificacion


def verify_encoded(encoded: str) -> tuple[bool, bytes | None]:
    try:
        # eliminar encabezado: "data:image/jpeg;base64,"
        if "," in encoded:
            encoded = encoded.split(",")[1]

        image = b64decode(encoded)
    except Exception as e:
        print(f"Error al decodificar la cadena Base64: {e}")
        return False, None

    try:
        image_stream = BytesIO(image)
        img = Image.open(image_stream)
        img.verify()
        return True, image

    except Exception as e:
        print(f"Error al verificar integridad de la imagen: {e}")
        return False, None


def save_image(encoded: str) -> Path | None:
    isValid, image = verify_encoded(encoded)

    if not isValid or not image:
        return None

    pictures_dir = Path("pictures")
    pictures_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4()}.jpg"
    final_path = pictures_dir / file_name

    # guardar
    try:
        with open(final_path, "wb") as f:
            f.write(image)

        # retornar la ruta absoluta
        return final_path.resolve(strict=True)
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return None


def build_content(data: Notificacion, file_path: Path) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = SMPTConfig.email
    msg["To"] = data.email
    msg["Subject"] = f"Notificación de Seguridad"
    file_name = file_path.name

    cuerpo = f"""
        Hola {data.nombre},

        Se ha registrado tu acceso en el sistema de seguridad a las {data.hora}. Adjunto encontrarás la evidencia fotográfica capturada.

        Si esta actividad no fue realizada por ti, por favor, contacta a soporte inmediatamente.

        Saludos, BeatAI.
        """

    msg.attach(MIMEText(cuerpo, "html"))

    try:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={file_name}",
        )

        msg.attach(part)

    except Exception as e:
        print(f"Error al adjuntar archivo: {e}")
        return msg

    return msg


def enviar_correo(data: Notificacion) -> Respuesta:
    file_path = save_image(data.b64)

    if not file_path:
        return Respuesta(success=False, error="Error al procesar la imagen")

    msg = build_content(data, file_path)

    # enviar correo
    with smtplib.SMTP(SMPTConfig.host, SMPTConfig.port) as server:
        server.starttls()
        server.login(SMPTConfig.email, SMPTConfig.password)
        server.sendmail(SMPTConfig.email, data.email, msg.as_string())

    file_path.unlink()  # eliminar la imagen
    print("Imagen eliminada")
    print(f"Correo enviado a {data.email}")

    return Respuesta(success=True)
