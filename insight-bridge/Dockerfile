FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Fix missing datetime import in nested bridge implementation at container build time without modifying source repo
RUN python -c "content = open('main.py').read(); open('main.py', 'w').write('import datetime\n' + content if 'import datetime' not in content else content)"

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/openapi.json || exit 1

CMD ["python", "main.py"]
