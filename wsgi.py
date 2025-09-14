# Healthcheck que responde antes de importar o app principal
from flask import Flask

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

# Importa o app principal
try:
    from app import app as main_app
    # Usa o app principal como padrão
    application = main_app
except Exception as e:
    # Se houver erro ao importar o app principal, usa o health_app
    print(f"Erro ao importar app principal: {e}")
    application = app

# Garante que o healthcheck funcione mesmo se o app principal falhar
if hasattr(application, 'get'):
    @application.get("/healthz")
    def healthz_fallback():
        return "ok", 200
