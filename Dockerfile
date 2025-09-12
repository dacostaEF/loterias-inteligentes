# Use Python 3.11 slim
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema mínimas (curl removido se não usar HEALTHCHECK)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Cache de deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY . .

# Exposição é opcional; Railway usa $PORT
EXPOSE 8000

# (Opcional) sem HEALTHCHECK no container; o Railway já checa /healthz
# Se quiser mesmo, instale curl e use: HEALTHCHECK ... curl -f http://127.0.0.1:$PORT/healthz

# Comando — ATENÇÃO: use $PORT do Railway
CMD ["bash", "-lc", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120"]
