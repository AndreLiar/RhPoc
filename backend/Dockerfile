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
    cat > /app/app/models/schemas.py << 'EOF'
from typing import List, Optional
from pydantic import BaseModel


class HRQueryRequest(BaseModel):
    question: str
    topic: Optional[str] = None  # optional manual override
    debug: bool = False


class Citation(BaseModel):
    source: str
    page: Optional[int] = None
    snippet: Optional[str] = None


class HRQueryResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    topic: Optional[str] = None
    intent: Optional[str] = None
    raw_context_count: int = 0
    debug_info: Optional[dict] = None
EOF

# Verify the models directory and files exist
RUN ls -la /app/app/ && \
    echo "=== Models directory contents ===" && \
    ls -la /app/app/models/ && \
    echo "=== schemas.py content ===" && \
    cat /app/app/models/schemas.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
