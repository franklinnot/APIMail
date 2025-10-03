import os
from dotenv import load_dotenv
from pydantic import BaseModel

# cargar variables de entorno
load_dotenv()


class Respuesta(BaseModel):
    success: bool
    error: str | None = None


class SMPTConfig:
    host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port: int = int(os.getenv("SMTP_PORT", 587))
    email: str = os.getenv("SMTP_EMAIL", "123@gmail.com")
    password: str = os.getenv("SMTP_PASSWORD", "123")
