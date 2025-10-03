from fastapi import FastAPI
from .dtos import Notificacion
from .classes import Respuesta
from .utils import enviar_correo

# cd app
# fastapi dev main.py

app = FastAPI(
    title="API de correos de BeatAI",
    description="API de correos de BeatAI, desarrollada para realizar notificaciones de seguridad.",
)


@app.get("/")
async def root() -> str:
    return app.description


@app.post("/send-email")
async def send_email(data: Notificacion) -> Respuesta:
    try:
        return enviar_correo(data)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return Respuesta(success=False, error=f"Hubo un error al enviar el correo.")
