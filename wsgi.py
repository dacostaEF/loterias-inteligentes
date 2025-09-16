# Healthcheck que responde antes de importar o app principal
from flask import Flask

# App mínimo só para healthcheck
health_app = Flask(__name__)

@health_app.get("/healthz")
def healthz():
    """Healthcheck super simples para Railway."""
    return "ok", 200

# Importa o app principal
try:
    from app import app as main_app
    # Usa o app principal como padrão
    application = main_app
    print("App principal importado com sucesso!")
    print(f"Total de rotas registradas: {len(application.url_map._rules)}")
    print("Rotas de API encontradas:")
    for rule in application.url_map.iter_rules():
        if 'api' in rule.rule:
            print(f"  {rule.rule} -> {rule.endpoint}")
except Exception as e:
    # Se houver erro ao importar o app principal, usa o health_app
    print(f"Erro ao importar app principal: {e}")
    import traceback
    traceback.print_exc()
    application = health_app

# Garante que o healthcheck funcione mesmo se o app principal falhar
if hasattr(application, 'add_url_rule'):
    try:
        @application.route("/healthz")
        def healthz_fallback():
            return "ok", 200
    except:
        pass  # Se já existir, ignora
