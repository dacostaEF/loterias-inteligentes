# Healthcheck que responde antes de importar o app principal
from flask import Flask

# App mínimo só para healthcheck
health_app = Flask(__name__)

@health_app.get("/healthz")
def healthz():
    """Healthcheck super simples para Railway."""
    return "ok", 200

@health_app.get("/")
def root():
    """Endpoint raiz simples."""
    return "Loterias Inteligentes - Online", 200

# Importa o app principal
try:
    from app import app
    # Usa o app principal como padrão
    application = app
except Exception as e:
    # Se houver erro ao importar o app principal, usa o health_app
    print(f"Erro ao importar app principal: {e}")
    application = health_app
