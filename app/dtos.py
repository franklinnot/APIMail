from pydantic import BaseModel


class Notificacion(BaseModel):
    nombre: str
    email: str
    hora: str
    b64: str
