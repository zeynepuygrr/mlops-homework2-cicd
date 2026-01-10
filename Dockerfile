FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# (Bazı paketler için gerekebilir)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI app + model artifact
COPY app ./app
COPY artifacts ./artifacts
COPY src ./src

# Default model path (override edilebilir)
ENV MODEL_PATH=/app/artifacts/model.joblib

EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]

