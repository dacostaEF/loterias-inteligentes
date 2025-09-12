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

<<<<<<< HEAD
# ⚠️ shell-form para expandir ${PORT}
CMD bash -lc "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120"
=======
# (Opcional) sem HEALTHCHECK no container; o Railway já checa /healthz
# Se quiser mesmo, instale curl e use: HEALTHCHECK ... curl -f http://127.0.0.1:$PORT/healthz

# Comando — ATENÇÃO: use $PORT do Railway
CMD bash -lc "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -"

>>>>>>> 315b20d788b6a64f1ad99ee2fae306b83da804d6
