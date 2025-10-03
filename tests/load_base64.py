import json
import sys
from pathlib import Path

PAYLOAD_FILE = Path(__file__).parent / "payload.json"


def load_base64():
    """Carga el Base64 desde el archivo JSON."""
    try:
        with open(PAYLOAD_FILE, "r") as f:
            data = json.load(f)
            return data.get("b64")
    except Exception as e:
        print(f"❌ ERROR: No se pudo cargar el Base64 de '{PAYLOAD_FILE}'. {e}")
        sys.exit(1)
