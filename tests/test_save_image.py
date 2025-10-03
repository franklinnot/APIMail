from app.utils import save_image
from tests.load_base64 import load_base64

# python -m tests.test_save_image

encoded = load_base64()
file_path = save_image(encoded)

if file_path:
    print(f"✅ Imagen guardada en: {file_path}")
else:
    print("❌ No se pudo guardar la imagen. Revisa el valor 'b64' en tu JSON.")

