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

# ⚠️ Comando para iniciar o servidor Gunicorn (CORRIGIDO)
# Usa uma sintaxe de shell para garantir que a variável de ambiente $PORT seja usada
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT} app:app --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -"
