import requests
import json
import time
import sys
import base64
from pathlib import Path

# python -m tests.test_api

URL = "http://127.0.0.1:8000/send-email"
PAYLOAD_FILE = Path(__file__).parent / "payload.json"


def load_json_data():
    try:
        with open(PAYLOAD_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Archivo '{PAYLOAD_FILE}' no encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"El archivo '{PAYLOAD_FILE}' no es un JSON válido.")
        sys.exit(1)


def get_dummy_b64() -> str:
    """Genera una imagen PNG mínima en base64 para pruebas."""
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode()


def test_api():
    payload = load_json_data()

    # permitir cambiar solo el email en cada prueba
    try:
        email_destino = input("Ingresa el email de destino: ").strip()
        if email_destino:
            payload["email"] = email_destino
    except EOFError:
        print("Operación cancelada.")
        sys.exit(1)

    # actualizar hora
    payload["hora"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # asegurar b64 válido
    if not payload.get("b64"):
        print("Payload sin 'b64', se genera dummy.")
        payload["b64"] = get_dummy_b64()

    print(f"\nEnviando payload a {URL} ...")
    print(json.dumps(payload, indent=2)[:500], "...")  # muestra solo inicio

    try:
        response = requests.post(URL, json=payload, timeout=15)
    except requests.exceptions.ConnectionError:
        print("API no disponible. Verifica que esté corriendo.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return

    print(f"\nCódigo de estado: {response.status_code}")
    try:
        print("Respuesta JSON:", response.json())
    except Exception:
        print("Respuesta cruda:", response.text)


test_api()
