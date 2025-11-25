FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files explicitly to ensure models directory is included
COPY app/ ./app/

# Create models directory and copy files explicitly if needed
RUN mkdir -p /app/app/models
COPY app/models/ ./app/models/

# Debug: List the directory structure
RUN echo "=== Directory structure ===" && \
    find /app -type f -name "*.py" | head -20 && \
    echo "=== End structure ===" && \
    ls -la /app/app/ && \
    ls -la /app/app/models/ && \
    echo "=== Python files in models ===" && \
    find /app/app/models -name "*.py" -exec ls -la {} \;

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
