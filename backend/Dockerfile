FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory with all subdirectories
COPY app ./app

# Debug: List the directory structure
RUN echo "=== Directory structure ===" && \
    find /app -type f -name "*.py" | head -20 && \
    echo "=== End structure ===" && \
    ls -la /app/app/ && \
    ls -la /app/app/models/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
