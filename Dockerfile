FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU first (separate index)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install app and OpenMed runtime dependencies from the same file used locally.
COPY healthadvocate/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY openmed/ ./openmed/
COPY healthadvocate/ ./healthadvocate/

# Default deployment is loopback-only (issue 72/80). Do not publish a
# non-loopback listener or unauthenticated reverse-proxy route by default.
EXPOSE 8080

CMD ["uvicorn", "healthadvocate.app:app", "--host", "127.0.0.1", "--port", "8080"]
