FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema (sqlite já vem OK, mas pode manter enxuto)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x start.sh

# IMPORTANTE: executar via /bin/sh
CMD ["/bin/sh", "-c", "./start.sh"]
