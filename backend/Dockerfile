FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory first
COPY app/ ./app/

# Create models directory and schemas.py manually to ensure it exists
RUN mkdir -p /app/app/models && \
    echo '# Models package' > /app/app/models/__init__.py && \
    echo 'from typing import List, Optional' > /app/app/models/schemas.py && \
    echo 'from pydantic import BaseModel' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo 'class HRQueryRequest(BaseModel):' >> /app/app/models/schemas.py && \
    echo '    question: str' >> /app/app/models/schemas.py && \
    echo '    topic: Optional[str] = None  # optional manual override' >> /app/app/models/schemas.py && \
    echo '    debug: bool = False' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo 'class Citation(BaseModel):' >> /app/app/models/schemas.py && \
    echo '    source: str' >> /app/app/models/schemas.py && \
    echo '    page: Optional[int] = None' >> /app/app/models/schemas.py && \
    echo '    snippet: Optional[str] = None' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo '' >> /app/app/models/schemas.py && \
    echo 'class HRQueryResponse(BaseModel):' >> /app/app/models/schemas.py && \
    echo '    answer: str' >> /app/app/models/schemas.py && \
    echo '    citations: List[Citation] = []' >> /app/app/models/schemas.py && \
    echo '    topic: Optional[str] = None' >> /app/app/models/schemas.py && \
    echo '    intent: Optional[str] = None' >> /app/app/models/schemas.py && \
    echo '    raw_context_count: int = 0' >> /app/app/models/schemas.py && \
    echo '    debug_info: Optional[dict] = None' >> /app/app/models/schemas.py

# Verify the models directory and files exist
RUN ls -la /app/app/ && \
    echo "=== Models directory contents ===" && \
    ls -la /app/app/models/ && \
    echo "=== schemas.py content ===" && \
    cat /app/app/models/schemas.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
