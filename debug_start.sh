#!/bin/bash
# Script de debug ULTRA SIMPLES

echo "=== ULTRA SIMPLE DEBUG ==="
echo "PORT variable: '$PORT'"
echo "PORT length: ${#PORT}"

# Se PORT não estiver definido, usar 5000
if [ -z "$PORT" ]; then
    echo "PORT not set, using 5000"
    PORT=5000
fi

echo "Final PORT: $PORT"

echo ""
echo "=== STARTING FLASK ==="
python -c "
from app import app
print('Flask app starting on port $PORT')
app.run(host='0.0.0.0', port=$PORT, debug=False)
"
