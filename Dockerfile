FROM python:3.11-slim

WORKDIR /app

# deps de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# deps Python (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código
COPY . .

# opcional: porta "documental"
EXPOSE 8000

# ⚠️ shell-form para expandir ${PORT}
CMD bash -lc "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120"
