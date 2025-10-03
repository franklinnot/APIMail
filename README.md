# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor
uvicorn main:app --reload

# guardar dependencias
pip freeze > requirements.txt

# ejecutar
fastapi dev app.main.py
fastapi run app.main.py

# 5. Probar con el cliente de test
python test.test.py
