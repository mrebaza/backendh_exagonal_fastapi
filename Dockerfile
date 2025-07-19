FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY ./src /app/src

EXPOSE 8000

# Comando por defecto para iniciar la API
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]