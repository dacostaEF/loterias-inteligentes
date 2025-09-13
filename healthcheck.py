#!/usr/bin/env python3
"""
Healthcheck super simples para Railway.
Responde imediatamente sem importar nada pesado.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    """Healthcheck super simples para Railway."""
    return "ok", 200

@app.route('/')
def root():
    """Endpoint raiz simples."""
    return "Loterias Inteligentes - Online", 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
