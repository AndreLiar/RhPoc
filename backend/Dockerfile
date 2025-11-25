FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory first
COPY app/ ./app/

# Verify the directory was copied and check if models exists
RUN ls -la /app/app/ && \
    echo "=== Checking for models directory ===" && \
    if [ -d "/app/app/models" ]; then \
        echo "✅ Models directory found"; \
        ls -la /app/app/models/; \
    else \
        echo "❌ Models directory missing - creating manually"; \
        mkdir -p /app/app/models; \
        echo "# Created by Dockerfile" > /app/app/models/__init__.py; \
    fi

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
