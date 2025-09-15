#!/usr/bin/env sh
set -eu

echo "=== STARTING LOTERIAS INTELIGENTES ==="
echo "Raw PORT env: ${PORT-<unset>}"

PORT="${PORT:-5000}"
echo "Final PORT: $PORT"

echo "PWD: $(pwd)"
python --version || true
env | grep -E '^(PORT|FLASK|PYTHON)=' || true

# Smoke tests (opcionais)
python -c "import healthcheck; print('healthcheck OK')" || echo "WARN: healthcheck import failed"
python -c "import wsgi; print('wsgi OK')" || echo "WARN: wsgi import failed"

echo "Starting gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --threads 2 \
  --timeout 30 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -
