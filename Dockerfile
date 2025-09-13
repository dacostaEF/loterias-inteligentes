FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# SQLite e toolchain básicos (mantenha se seu app usa sqlite / compila algo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev sqlite3 build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
ENV PORT=5000

# (Opcional) healthcheck interno pra depurar local
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD \
  python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${PORT}/healthz').read()" || exit 1

# 👇 usa shell pra expandir ${PORT}
CMD ["sh","-c","exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -"]
