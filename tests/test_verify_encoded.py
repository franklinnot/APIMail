from app.correo_service import verify_encoded
from tests.load_base64 import load_base64

# python -m tests.test_verify_encoded

encoded = load_base64()
isValid = verify_encoded(encoded)

if isValid:
    print("La imagen es válida.")
else:
    print("La imagen no es válida.")
