#!/bin/bash
# Script de debug para identificar o problema

echo "=== DEBUG START ==="
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

echo ""
echo "=== ENVIRONMENT VARIABLES ==="
echo "PORT: '$PORT'"
echo "PATH: '$PATH'"
echo "PYTHONPATH: '$PYTHONPATH'"

echo ""
echo "=== PYTHON VERSION ==="
python --version

echo ""
echo "=== CHECKING WSGI FILE ==="
if [ -f "wsgi.py" ]; then
    echo "wsgi.py exists"
    echo "Content of wsgi.py:"
    cat wsgi.py
else
    echo "wsgi.py NOT FOUND!"
fi

echo ""
echo "=== CHECKING APP.PY ==="
if [ -f "app.py" ]; then
    echo "app.py exists"
    echo "Size: $(wc -l < app.py) lines"
else
    echo "app.py NOT FOUND!"
fi

echo ""
echo "=== TESTING PYTHON IMPORT ==="
python -c "
try:
    from app import app
    print('✅ app.py import successful')
    print('App type:', type(app))
except Exception as e:
    print('❌ app.py import failed:', str(e))
"

echo ""
echo "=== TESTING WSGI IMPORT ==="
python -c "
try:
    from wsgi import app
    print('✅ wsgi.py import successful')
    print('App type:', type(app))
except Exception as e:
    print('❌ wsgi.py import failed:', str(e))
"

echo ""
echo "=== TESTING GUNICORN COMMAND ==="
echo "Command that will be executed:"
echo "gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -"

echo ""
echo "=== STARTING GUNICORN ==="
exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 --log-level info --access-logfile - --error-logfile -
