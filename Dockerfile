FROM python:3.13-slim

# Variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copiamos dependencias
COPY requirements.txt .

# Instalamos con psycopg moderno (tu URL lo necesita)
RUN pip install --upgrade pip setuptools wheel \
    && pip install "psycopg[binary]" \
    && pip install -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Exponemos el puerto para Railway
EXPOSE 8000

# Comando final: Uvicorn ASGI directo
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
