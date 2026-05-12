FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for tokenizers
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu \
    transformers>=4.50 \
    huggingface-hub>=0.30 \
    accelerate>=0.29 \
    tokenizers>=0.15 \
    pysbd>=0.3.4 \
    faker>=22.0 \
    fastapi>=0.104.0 \
    "uvicorn[standard]>=0.24.0" \
    pydantic>=2.0.0

COPY openmed/ ./openmed/
COPY healthadvocate/ ./healthadvocate/

EXPOSE 8080

CMD ["uvicorn", "healthadvocate.app:app", "--host", "0.0.0.0", "--port", "8080"]
