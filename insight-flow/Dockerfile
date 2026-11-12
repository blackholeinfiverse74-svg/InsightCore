FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Ensure bucket directories exist both at /app/bucket and /bucket (since os.path.join(..., "..", "bucket") resolves to /bucket)
RUN mkdir -p /app/bucket /bucket && ln -sf /app/bucket /bucket

EXPOSE 8002

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8002/openapi.json || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
