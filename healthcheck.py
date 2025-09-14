#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Healthcheck mínimo para Railway
"""

from flask import Flask
import os

# App mínimo só para healthcheck
app = Flask(__name__)

@app.get("/healthz")
def healthz():
    """Healthcheck super simples para Railway."""
    return "ok", 200

@app.get("/")
def root():
    """Endpoint raiz simples."""
    return "Loterias Inteligentes - Online", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)