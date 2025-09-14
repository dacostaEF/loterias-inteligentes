#!/bin/bash

# Script de inicialização robusto para Railway
echo "=== INICIANDO LOTERIAS INTELIGENTES ==="
echo "PORT: $PORT"
echo "PWD: $(pwd)"
echo "Python version: $(python --version)"
echo "Environment variables:"
env | grep -E "(PORT|FLASK|PYTHON)" | sort

# Se PORT não estiver definido, usar 5000
if [ -z "$PORT" ]; then
    echo "PORT não definido, usando 5000"
    PORT=5000
fi

echo "Porta final: $PORT"

# Testa se o Python consegue importar o módulo
echo "Testando import do healthcheck..."
python -c "import healthcheck; print('Healthcheck importado com sucesso')" || echo "ERRO: Não conseguiu importar healthcheck"

# Testa se o Python consegue importar o app principal
echo "Testando import do app principal..."
python -c "import app; print('App principal importado com sucesso')" || echo "ERRO: Não conseguiu importar app principal"

# Testa se o Python consegue importar o wsgi
echo "Testando import do wsgi..."
python -c "import wsgi; print('WSGI importado com sucesso')" || echo "ERRO: Não conseguiu importar wsgi"

# Inicia o gunicorn com healthcheck:app
echo "Iniciando gunicorn..."
exec gunicorn healthcheck:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 2 \
    --timeout 30 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
