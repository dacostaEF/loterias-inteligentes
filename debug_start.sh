#!/bin/bash
# Script de debug SIMPLES

echo "=== SIMPLE DEBUG START ==="
echo "PORT: '$PORT'"
echo "PWD: $(pwd)"
echo "Files:"
ls -la

echo ""
echo "=== TESTING PYTHON ==="
python -c "print('Python works!')"

echo ""
echo "=== TESTING APP IMPORT ==="
python -c "
try:
    from app import app
    print('App import OK')
except Exception as e:
    print('App import ERROR:', e)
"

echo ""
echo "=== STARTING SIMPLE SERVER ==="
python -c "
from app import app
print('Starting Flask app...')
app.run(host='0.0.0.0', port=int('$PORT' or 5000), debug=False)
"
