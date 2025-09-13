# Usa uma imagem base Python com o Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o contêiner
COPY . .

# Expõe a porta que o Gunicorn vai rodar
EXPOSE 5000

# Healthcheck (opcional, ajuda na depuração)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD \
  python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${PORT}/healthz').read()" || exit 1

# 👇 Shell para expandir ${PORT}
CMD ["sh", "-c", "exec gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -"]
